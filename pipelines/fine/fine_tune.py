import asyncio
import json
import os
import sys
from typing import Dict

from loguru import logger

from pipe.add_symb_schema import AddSymbolicSchema
from pipe.attack import Attack
from pipe.copy_transformer import DeleteProp
from pipe.pipeline import Pipeline
from pipe.processor.limit_list import FilterList
from pipe.processor.list_transformer import JsonListTransformer
from pipe.processor.print_results import PrintResults
from pipe.schema_repo import DatabaseSchemaRepo
from pipe.symb_table import AddSymbolTable
from pipelines.fine.gold_mask import MaskWithGoldData
from pipelines.fine.repair_schema_links import RepairGoldLinks, AddExplicitLinks

LLM_MODEL = os.getenv("LLM_MODEL")
SLM_MODEL = os.getenv("SLM_MODEL")
VLM_MODEL = os.getenv("VLM_MODEL")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

out_dir = os.path.join("out", "fine")

if not os.path.exists(out_dir):
    os.makedirs(out_dir, exist_ok=True)

database_path = "../parser/data/bird/database"
input_path = os.path.join(out_dir, "1_input.json")
tables_path = os.path.join(out_dir, "tables.json")


class AddId(JsonListTransformer):
    def __init__(self):
        super().__init__()
        self.idx = 0

    async def _process_row(self, row: Dict) -> Dict:
        row['idx'] = self.idx
        self.idx += 1
        return row


class AddExpLinksAsDict(JsonListTransformer):
    def __init__(self, tables_path):
        super().__init__()
        self.schema_repo = DatabaseSchemaRepo(tables_path)

    async def _process_row(self, row: Dict) -> Dict:
        links = row['exp_links']
        schema = self.schema_repo.dbs[row['db_id']]
        reference_links = dict()
        for link in links:
            link_ref = f"[{link.lower()}]"
            for table, cols in schema.tables.items():
                if link_ref == table.lower():
                    reference_links[table] = f"TABLE:{table}"
                    break
                for col, _ in cols.items():
                    if link_ref == col.lower():
                        reference_links[link] = f"COLUMN:{table}.{col}"
                        break
        row['ref_links'] = reference_links
        return row


class MergeLinks(JsonListTransformer):

    async def _process_row(self, row: Dict) -> Dict:
        gold_links = row['gold_links']
        repaired_links = row['repaired_links']
        ref_links = row['ref_links']
        final_links = {**repaired_links, **gold_links, **ref_links}
        row['final_links'] = final_links
        return row


class Unwind(JsonListTransformer):

    async def _process_row(self, row: Dict) -> Dict:
        if 'question_id' in row:
            return row
        idx = row['idx']
        gold_links = row['gold_links']
        repaired_links = row['repaired_links']
        new_row = dict()
        new_row['idx'] = idx
        new_row['question'] = row['question']
        new_row['masked'] = row['symbolic']['question']
        new_row['sql'] = row['query']
        new_row['final_links'] = row['final_links']
        new_row['exp_links'] = row['exp_links']
        new_row['to_name'] = row['symbolic']['to_name']
        new_row['attack'] = row['attack']
        with open(f"out/fine/unwinds/{idx}.json", "w") as f:
            f.write(json.dumps(new_row, indent=4))
        return row


pl = [
    FilterList(lambda row: 'question_id' not in row),
    RepairGoldLinks('repaired_links', model="gpt-4.1"),
    AddExplicitLinks('exp_links', model="gpt-4.1"),
    AddExpLinksAsDict(tables_path),
    MergeLinks(),
    AddSymbolTable(tables_path),
    AddSymbolicSchema(tables_path),
    MaskWithGoldData(),
    DeleteProp('attack'),
    Attack("attack", model=LLM_MODEL),
    FilterList(lambda row: row['eval']['acc'] == 0),
    Unwind(),
    # PrintResults()
    # Inspector()
]


async def main():
    try:
        logger.remove(0)
    except Exception:
        pass
    logger.add(sys.stderr, level=LOG_LEVEL, colorize=True, enqueue=True,
               format="<green>{time:HH:mm:ss}[{process.id}] | </green><level> {level}: {message}</level>")

    pipeline = Pipeline(pl)
    out_path = await pipeline.run(input_path)
    print("LLM MODEL:", LLM_MODEL)
    print("SLM MODEL:", SLM_MODEL)


if __name__ == '__main__':
    asyncio.run(main())

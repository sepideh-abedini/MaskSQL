import asyncio
import os
from typing import Dict

from pipe.add_schema import AddSchema
from pipe.add_symb_schema import AddSymbolicSchema
from pipe.pipeline import Pipeline
from pipe.processor.list_transformer import JsonListTransformer
from pipe.symb_table import AddSymbolTable
from pipelines.fine.fine_tune import AddId, AddExpLinksAsDict
from pipelines.fine.repair_schema_links import RepairGoldLinks, AddExplicitLinks
from src.cat.catter import Catter
from ut.json_utils import read_json, write_json

catter = Catter()

out_dir = os.path.join("out", "fine", "bird_train_sel")
input_path = os.path.join(out_dir, "1_input.json")
tables_path = os.path.join(out_dir, "tables.json")


class TablesExtractor(JsonListTransformer):
    def __init__(self):
        super().__init__()
        self.dbs = set()

    def _post_run(self):
        tables = read_json(os.path.join(out_dir, "tables.json"))
        selected_tables = []
        for t in tables:
            if t['db_id'] in self.dbs:
                selected_tables.append(t)
        write_json(os.path.join(out_dir, 'sel_tables.json'), selected_tables)

    async def _process_row(self, row: Dict) -> Dict:
        db_id = row['db_id']
        self.dbs.add(db_id)
        return row


class FixFormat(JsonListTransformer):

    async def _process_row(self, row: Dict) -> Dict:
        row['query'] = row['SQL']
        row['question'] = row['question'] + " " + row['evidence']
        del row['SQL']
        return row


class Unwind(JsonListTransformer):
    def __init__(self):
        super().__init__()
        self.data = read_json("out/bird/18_ExecAccCalc.json")
        os.makedirs("out/fine/unwinds", exist_ok=True)

    async def _process_row(self, row: Dict) -> Dict:
        if 'question_id' in row:
            return row
        idx = row['idx']
        result = self.data[idx]
        assert result['question'] == row['question']
        if result['eval']['acc'] == 1:
            return row
        new_row = dict()
        new_row['idx'] = idx
        new_row['question'] = row['question']
        new_row['sql'] = row['query']
        new_row['cat'] = row['cat']
        new_row['final_links'] = row['final_links']
        write_json(f"out/fine/unwinds/{idx}.json", new_row)
        return row


class MergeLinks(JsonListTransformer):

    async def _process_row(self, row: Dict) -> Dict:
        gold_links = row['gold_links']
        ref_links = row['ref_links']
        final_links = {**gold_links, **ref_links}
        row['final_links'] = final_links
        return row



async def main():
    pl = [
        AddSchema(tables_path),
        RepairGoldLinks('gold_links', model="gpt-4.1"),
        AddExplicitLinks('exp_links', model="gpt-4.1"),
        AddId(),
        AddExpLinksAsDict(tables_path),
        MergeLinks(),
        AddSymbolTable(tables_path),
        AddSymbolicSchema(tables_path),
        Unwind(),
    ]

    pipeline = Pipeline(pl)
    await pipeline.run(input_path)


if __name__ == '__main__':
    asyncio.run(main())

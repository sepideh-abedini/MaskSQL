import asyncio
import os
import sys
from typing import Dict

from loguru import logger

from pipe.add_schema import AddSchema
from pipe.gen_gold_schema import GenGoldLinks
from pipe.pipeline import Pipeline
from pipe.processor.limit_list import LimitJson
from pipe.processor.list_transformer import JsonListTransformer
from pipelines.fine.bird_train_annon import MergeLinks, Unwind
from pipelines.fine.fine_tune import AddExpLinksAsDict
from pipelines.fine.repair_schema_links import AddExplicitLinks, RepairGoldLinks
from ut.json_utils import write_json, read_json

LLM_MODEL = os.getenv("LLM_MODEL")
SLM_MODEL = os.getenv("SLM_MODEL")
VLM_MODEL = os.getenv("VLM_MODEL")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

out_dir = os.path.join("out", "latest", "gold_links")

if not os.path.exists(out_dir):
    os.makedirs(out_dir, exist_ok=True)

database_path = "../parser/data/bird/database"
input_path = os.path.join(out_dir, "1_input.json")
tables_path = os.path.join(out_dir, "tables.json")


class CleanData(JsonListTransformer):

    async def _process_row(self, row: Dict) -> Dict:
        del row['eval']
        del row['schema']
        del row['pred_sql']
        row['total_latency'] = 0
        row['total_toks'] = 0
        return row


class Unwind(JsonListTransformer):
    def __init__(self):
        super().__init__()
        self.dir = os.path.join(out_dir, "unwind")
        os.makedirs(self.dir, exist_ok=True)

    async def _process_row(self, row: Dict) -> Dict:
        new_row = dict()
        idx = row['question_id']
        new_row['question'] = row['question']
        new_row['sql'] = row['query']
        new_row['final_links'] = row['final_links']
        write_json(os.path.join(self.dir, f"{idx}.json"), new_row)
        return row


class CollectUnwinds(JsonListTransformer):
    def __init__(self):
        super().__init__()
        self.dir = os.path.join(out_dir, "annotated")

    async def _process_row(self, row: Dict) -> Dict:
        idx = row['question_id']
        try:
            data = read_json(os.path.join(self.dir, f"{idx}.json"))
            row['annotated_links'] = data['final_links']
        except Exception as e:
            print(idx)
        return row


class RemoveDuplicates(JsonListTransformer):

    async def _process_row(self, row: Dict) -> Dict:
        refined_links = dict()
        final_links = row['final_links']
        question = row['question'].lower()

        for q_term, item in final_links.items():
            q_term = q_term.lower()
            if q_term in refined_links:
                continue
            if q_term not in question:
                continue
            refined_links[q_term] = item
        row['final_links'] = refined_links
        return row


mask_pipe = [
    LimitJson("limit"),
    # AddSchema(tables_path),
    # GenGoldLinks("gold_links", model="gpt-4.1"),
    # RepairGoldLinks('gold_links', model="gpt-4.1"),
    # AddExplicitLinks('exp_links', model="gpt-4.1"),
    # AddExpLinksAsDict(tables_path),
    # MergeLinks(),
    # RemoveDuplicates(),
    # Unwind(),
    CollectUnwinds()
]


async def main():
    try:
        logger.remove(0)
    except Exception:
        pass
    logger.add(sys.stderr, level=LOG_LEVEL, colorize=True, enqueue=True,
               format="<green>{time:HH:mm:ss}[{process.id}] | </green><level> {level}: {message}</level>")

    pipeline = Pipeline(mask_pipe)
    out_path = await pipeline.run(input_path)
    print("LLM MODEL:", LLM_MODEL)
    print("SLM MODEL:", SLM_MODEL)


if __name__ == '__main__':
    asyncio.run(main())

import asyncio
import os
import sys
from typing import Dict

from loguru import logger

from pipe.pipeline import Pipeline
from pipe.processor.limit_list import FilterList
from pipe.processor.list_transformer import JsonListTransformer
from pipelines.eval import Results
from ut.json_utils import read_json

out_dir = os.path.join("out", "latest", "msc")

if not os.path.exists(out_dir):
    os.makedirs(out_dir, exist_ok=True)

database_path = "../parser/data/bird/database"
input_path = os.path.join(out_dir, "1_input.json")
tables_path = os.path.join(out_dir, "tables.json")


class FilterOutputs(FilterList):
    def __init__(self):
        super().__init__(self.is_good)
        ref_data = read_json(os.path.join(out_dir, "ref.json"))
        self.good_ids = set(map(lambda r: r['question_id'], ref_data))

    def is_good(self, row):
        return row['question_id'] in self.good_ids


class AddTokenTime(JsonListTransformer):
    def __init__(self):
        super().__init__()
        N = 1028

    # async def _process_row(self, row: Dict) -> Dict:


pipe = [
    # Results(),
    FilterOutputs(),
    Results()
]


async def main():
    try:
        logger.remove(0)
    except Exception:
        pass
    logger.add(sys.stderr, level="INFO", colorize=True, enqueue=True,
               format="<green>{time:HH:mm:ss}[{process.id}] | </green><level> {level}: {message}</level>")

    pipeline = Pipeline(pipe)
    out_path = await pipeline.run(input_path)


if __name__ == '__main__':
    asyncio.run(main())

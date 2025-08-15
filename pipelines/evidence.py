import asyncio
import os
import sys
from typing import Dict

from loguru import logger

from pipe.pipeline import Pipeline
from pipe.processor.limit_list import FilterList
from pipe.processor.list_transformer import JsonListTransformer
from pipelines.eval import Results
from pipelines.fine.bird_extractor import Counter

out_dir = os.path.join("out", "final_v3")

if not os.path.exists(out_dir):
    os.makedirs(out_dir, exist_ok=True)

database_path = "../parser/data/bird/database"
input_path = os.path.join(out_dir, "1_input.json")
tables_path = os.path.join(out_dir, "tables.json")


class AddEvidence(JsonListTransformer):
    def __init__(self):
        super().__init__()

    async def _process_row(self, row: Dict) -> Dict:
        evidence = row['evidence']
        question = row['question']
        row['question'] = f"{question} {evidence}"
        row['evidence_added'] = True
        return row


pipe = [
    AddEvidence(),
    Counter()
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

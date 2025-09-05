import asyncio
import os
import sys
from typing import Dict

from loguru import logger

from src.pipe import Pipeline
from src.pipe.processor.list_transformer import JsonListTransformer

out_dir = os.path.join("out", "new_dataset_bad")

if not os.path.exists(out_dir):
    os.makedirs(out_dir, exist_ok=True)

database_path = "../parser/data/bird/database"
input_path = os.path.join(out_dir, "1_input.json")
tables_path = os.path.join(out_dir, "tables.json")


class FixFormat(JsonListTransformer):
    def __init__(self):
        super().__init__()

    async def _process_row(self, row: Dict) -> Dict:
        row['query'] = row['SQL']
        row['msc_ea'] = row['eval']['acc']
        del row['eval']
        del row['gold']
        del row['pred']
        return row


pipe = [
    FixFormat()
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

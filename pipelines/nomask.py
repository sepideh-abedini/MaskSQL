import asyncio
import os
import sys
from typing import Dict

from loguru import logger

from pipe.add_schema import AddSchema
from pipe.exec_acc import ExecAccCalc
from pipe.gen_sql import GenSql
from pipe.pipeline import Pipeline
from pipe.processor.list_transformer import JsonListTransformer
from pipe.processor.print_results import PrintResults
from pipelines.eval import Results

out_dir = os.path.join("out", "latest_qwen")

if not os.path.exists(out_dir):
    os.makedirs(out_dir, exist_ok=True)

database_path = "../parser/data/bird/database"
input_path = os.path.join(out_dir, "1_input.json")
tables_path = os.path.join(out_dir, "tables.json")


class FixFormat(JsonListTransformer):

    async def _process_row(self, row: Dict) -> Dict:
        row['query'] = row['SQL']
        return row


pipe = [
    AddSchema(tables_path),
    GenSql('pred_sql', model="qwen"),
    ExecAccCalc(database_path),
    PrintResults()
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

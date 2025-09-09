import asyncio
import os
import sys
from typing import Dict

from loguru import logger

from src.pipe.add_schema import AddFilteredSchema
from src.pipe import AddSymbolicSchema
from src.pipe import CopyTransformer
from src.pipe import AddSymbolicQuestion
from src.pipe import DetectValues
from src.pipe.exec_acc import CalcExecAcc
from src.pipe.gen_masked_sql import GenerateSymbolicSql
from src.pipe import LinkSchema
from src.pipe import Pipeline
from src.pipe.processor import LimitJson
from src.pipe.processor.list_transformer import JsonListTransformer
from src.pipe import RankSchemaResd
from src.pipe import RepairSQL
from src.pipe import RepairSymbolicSQL
from src.pipe import AddSymbolTable
from src.pipe import AddConcreteSql
from src.pipe import LinkValues
from src.pipe import WrongExecAccOutput
from pipelines.eval import Results
from ut.json_utils import read_json

LLM_MODEL = os.getenv("LLM_MODEL")
SLM_MODEL = os.getenv("SLM_MODEL")
VLM_MODEL = os.getenv("VLM_MODEL")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

out_dir = os.path.join("out", "latest", "trust_full_tmp")

if not os.path.exists(out_dir):
    os.makedirs(out_dir, exist_ok=True)

database_path = "../parser/data/bird/database"
input_path = os.path.join(out_dir, "1_input.json")
tables_path = os.path.join(out_dir, "tables.json")


class FixFormat(JsonListTransformer):

    async def _process_row(self, row: Dict) -> Dict:
        row['query'] = row['SQL']
        return row


class AddResd(JsonListTransformer):
    def __init__(self, out_dirc):
        super().__init__()
        self.resd = read_json(os.path.join(out_dirc, "resdsql_test.json"))
        self.idx = 0

    async def _process_row(self, row: Dict) -> Dict:
        row['tc_original'] = self.resd[self.idx]['tc_original']
        self.idx += 1
        return row


mask_pipe = [
    LimitJson("limit"),
    AddResd(out_dir),
    RankSchemaResd(tables_path),
    # AddSchemaItems(tables_path),
    AddFilteredSchema(tables_path),
    # GenGoldLinks("gold_links", model=LLM_MODEL),
    AddSymbolTable(tables_path),
    DetectValues("values", model=SLM_MODEL),
    LinkValues("value_links", model=SLM_MODEL),
    CopyTransformer("value_links", "filtered_value_links"),
    LinkSchema("schema_links", model=SLM_MODEL),
    CopyTransformer("schema_links", "filtered_schema_links"),
    AddSymbolicSchema(tables_path),
    AddSymbolicQuestion(),
    # Attack("attack", model=LLM_MODEL),
    GenerateSymbolicSql("symbolic", model=LLM_MODEL),
    RepairSymbolicSQL('symbolic', model=LLM_MODEL),
    AddConcreteSql(),
    WrongExecAccOutput(database_path),
    RepairSQL('pred_sql', model=SLM_MODEL),
    CalcExecAcc(database_path),
    # Attack("attack", model=LLM_MODEL),
    Results()
    # PrintResults()
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

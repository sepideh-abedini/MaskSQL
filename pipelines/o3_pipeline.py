import asyncio
import os
import sys

from loguru import logger

from pipe.add_schema import AddFilteredSchema
from pipe.add_symb_schema import AddSymbolicSchema
from pipe.copy_transformer import CopyTransformer
from pipe.det_mask import AddSymbolicQuestion
from pipe.detect_entities import DetectValues
from pipe.exec_acc import ExecAccCalc
from pipe.gen_masked_sql import GenerateSymbolicSql
from pipe.link_schema import LinkSchema
from pipe.pipeline import Pipeline
from pipe.processor.limit_list import LimitJson
from pipe.processor.print_results import PrintResults
from pipe.rank_schema import RankSchemaResd
from pipe.repair_sql import RepairSQL
from pipe.repair_symb_sql import RepairSymbolicSQL
from pipe.symb_table import AddSymbolTable
from pipe.unmask import AddConcreteSql
from pipe.value_links import LinkValues
from pipe.wrong_exec_acc import WrongExecAccOutput

LLM_MODEL = os.getenv("LLM_MODEL")
SLM_MODEL = os.getenv("SLM_MODEL")
ALT_MODEL = os.getenv("ALT_MODEL")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

out_dir = os.path.join("out", "o3", "0_base")
# out_dir = os.path.join("out", "o3", "4_repair")

if not os.path.exists(out_dir):
    os.makedirs(out_dir, exist_ok=True)

database_path = "../parser/data/bird/database"
input_path = os.path.join(out_dir, "1_input.json")
tables_path = os.path.join(out_dir, "tables.json")

mask_pipe = [
    LimitJson("limit"),
    RankSchemaResd(tables_path),
    AddFilteredSchema(tables_path),
    AddSymbolTable(tables_path),
    DetectValues("values", model=SLM_MODEL),
    LinkValues("value_links", model=SLM_MODEL),
    CopyTransformer("value_links", "filtered_value_links"),
    LinkSchema("schema_links", model=SLM_MODEL),
    CopyTransformer("schema_links", "filtered_schema_links"),
    AddSymbolicSchema("symbolic", tables_path),
    AddSymbolicQuestion(),
    GenerateSymbolicSql("symbolic", model=LLM_MODEL),
    RepairSymbolicSQL('symbolic', model=LLM_MODEL),
    AddConcreteSql(),
    WrongExecAccOutput(database_path),
    RepairSQL('pred_sql', model=SLM_MODEL),
    ExecAccCalc(database_path),
    PrintResults()
]


async def main():
    try:
        logger.remove(0)
    except Exception:
        pass
    logger.add(sys.stderr, level=LOG_LEVEL, colorize=True, enqueue=True,
               format="<green>{time:HH:mm:ss}[{process.id}] | </green><level> {level}: {message}</level>")

    pipeline = Pipeline(mask_pipe)
    await pipeline.run(input_path)
    print("LLM MODEL:", LLM_MODEL)
    print("SLM MODEL:", SLM_MODEL)


if __name__ == '__main__':
    asyncio.run(main())

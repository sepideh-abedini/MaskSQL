import asyncio
import os
import sys

from loguru import logger

from pipe.add_masked_terms import AddMaskedTerms
from pipe.add_schema import AddFilteredSchema, AddSchema, AddSchemaItems
from pipe.add_symb_schema import AddSymbolicSchema
from pipe.add_value_links_from_schema_links import AddValueLinksFromSchemaLinks
from pipe.attack import Attack, AttackRaw
from pipe.copy_transformer import CopyTransformer
from pipe.det_mask import AddSymbolicQuestion
from pipe.detect_entities import DetectValues, DetectValuesDummy
from pipe.exec_acc import ExecAccCalc
from pipe.gen_gold_schema import GenGoldLinks
from pipe.gen_masked_sql import GenerateSymbolicSql
from pipe.gen_masked_sql_raw import GenerateSymbolicSqlRaw
from pipe.link_schema import LinkSchema
from pipe.link_schema_and_value import LinkSchemaAndValue
from pipe.pipeline import Pipeline
from pipe.processor.limit_list import LimitJson
from pipe.processor.print_results import PrintResults
from pipe.processor.printer import CustomPrinter
from pipe.processor.privacy_score import PrivacyScore
from pipe.processor.schema_link_score import SchemaLinkScore
from pipe.rank_schema import RankSchemaResd
from pipe.repair_sql import RepairSQL
from pipe.repair_symb_sql import RepairSymbolicSQL, RepairSymbolicSQLRaw
from pipe.slm_mask import SlmMask, SlmUnmask
from pipe.slm_mask_for_det_unmask import SlmMaskWithSymbolTable
from pipe.slm_unmask_repair import SlmUnmaskAndRepair
from pipe.symb_table import AddSymbolTable, AddValueSymbolTable
from pipe.unmask import AddConcreteSql
from pipe.value_links import LinkValues
from pipe.wrong_exec_acc import WrongExecAccOutput

LLM_MODEL = os.getenv("LLM_MODEL")
LINK_MODEL = os.getenv("LINK_MODEL")
REPAIR_MODEL = os.getenv("REPAIR_MODEL")
PRIVATE_MODEL = os.getenv("PRIVATE_MODEL")
SLM_MODEL = os.getenv("SLM_MODEL")
ALT_MODEL = os.getenv("ALT_MODEL")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

out_dir = os.path.join("out", "paper", "1_test")

if not os.path.exists(out_dir):
    os.makedirs(out_dir, exist_ok=True)

database_path = "../parser/data/bird/database"
input_path = os.path.join(out_dir, "1_input.json")
tables_path = os.path.join(out_dir, "tables.json")
output_path = os.path.join(out_dir, "output.json")
eval_path = os.path.join(out_dir, "eval.json")

mask_pipe = [
    LimitJson("limit"),
    RankSchemaResd(tables_path),
    AddFilteredSchema(tables_path),
    AddSymbolTable(tables_path),
    CopyTransformer("schema_links", "filtered_schema_links"),
    AddSymbolicSchema("symbolic", tables_path),
    AddSymbolicQuestion(),
    CustomPrinter()
]

slm_mask = [
    LimitJson("limit"),
    RankSchemaResd(tables_path),
    AddFilteredSchema(tables_path),
    GenGoldLinks("gold_links", model=LLM_MODEL),
    SlmMask("symbolic", model=SLM_MODEL),
    AttackRaw("attack", model=LLM_MODEL),
    GenerateSymbolicSqlRaw("symbolic", model=LLM_MODEL),
    RepairSymbolicSQLRaw('symbolic', model=LLM_MODEL),
    SlmUnmask("concrete_sql", model=SLM_MODEL),
    WrongExecAccOutput(database_path),
    RepairSQL('pred_sql', model=REPAIR_MODEL),
    ExecAccCalc(database_path),
    PrivacyScore(),
    PrintResults(),
]


async def main():
    try:
        logger.remove(0)
    except Exception:
        pass
    logger.add(sys.stderr, level=LOG_LEVEL, colorize=True, enqueue=True,
               format="<green>{time:HH:mm:ss}[{process.id}] | </green><level> {level}: {message}</level>")

    pipeline = Pipeline(mask_pipe)
    # pipeline = Pipeline(slm_mask)

    out_path = await pipeline.run(input_path)
    print("LLM MODEL:", LLM_MODEL)
    print("SLM MODEL:", SLM_MODEL)
    # print("LINK MODEL:", LINK_MODEL)
    # print("REPAIR MODEL:", REPAIR_MODEL)


if __name__ == '__main__':
    asyncio.run(main())

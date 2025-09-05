import asyncio
import os
import sys

from loguru import logger

from src.pipe.add_schema import AddFilteredSchema
from src.pipe.add_symb_schema import AddSymbolicSchema
from src.pipe.attack import AddInferenceAttack, AttackRaw
from src.pipe.copy_transformer import CopyTransformer
from src.pipe.det_mask import AddSymbolicQuestion
from src.pipe.detect_entities import DetectValues
from src.pipe.exec_acc import CalcExecAcc
from src.pipe.gen_gold_schema import GenGoldLinks
from src.pipe.gen_masked_sql import GenerateSymbolicSql
from src.pipe.gen_masked_sql_raw import GenerateSymbolicSqlRaw
from src.pipe.link_schema import LinkSchema
from src.pipe.pipeline import Pipeline
from src.pipe.processor.limit_list import LimitJson
from src.pipe.processor.print_results import PrintResults
from src.pipe.processor.privacy_score import PrivacyScore
from src.pipe.rank_schema import RankSchemaResd
from src.pipe.repair_sql import RepairSQL
from src.pipe.repair_symb_sql import RepairSymbolicSQL, RepairSymbolicSQLRaw
from src.pipe.slm_mask import SlmMask, SlmUnmask
from src.pipe.symb_table import AddSymbolTable
from src.pipe.unmask import AddConcreteSql
from src.pipe.value_links import LinkValues
from src.pipe.wrong_exec_acc import ExecuteConcreteSql

LLM_MODEL = os.getenv("LLM_MODEL")
LINK_MODEL = os.getenv("LINK_MODEL")
REPAIR_MODEL = os.getenv("REPAIR_MODEL")
PRIVATE_MODEL = os.getenv("PRIVATE_MODEL")
SLM_MODEL = os.getenv("SLM_MODEL")
ALT_MODEL = os.getenv("ALT_MODEL")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

out_dir = os.path.join("out", "ablation", "1_perfect_base_new")

if not os.path.exists(out_dir):
    os.makedirs(out_dir, exist_ok=True)

database_path = "../parser/data/bird/database"
input_path = os.path.join(out_dir, "1_input.json")
tables_path = os.path.join(out_dir, "tables.json")
output_path = os.path.join(out_dir, "output.json")
eval_path = os.path.join(out_dir, "eval.json")

mask_pipe = [
    LimitJson(),
    RankSchemaResd(tables_path),
    AddFilteredSchema(tables_path),
    GenGoldLinks("gold_links", model=LLM_MODEL),
    CopyTransformer("question", "bar"),
    AddSymbolTable(tables_path),
    DetectValues("values", model=SLM_MODEL),
    LinkValues("value_links", model=SLM_MODEL),
    CopyTransformer("value_links", "filtered_value_links"),
    # AddValueSymbolTable(tables_path),
    LinkSchema("schema_links", model=SLM_MODEL),
    CopyTransformer("schema_links", "filtered_schema_links"),
    AddSymbolicSchema("symbolic", tables_path),
    AddSymbolicQuestion(),
    # SlmMaskWithSymbolTable("symbolic", model=SLM_MODEL),
    AddInferenceAttack("attack", model=LLM_MODEL),
    GenerateSymbolicSql("symbolic", model=LLM_MODEL),
    # CopyTransformer("symbolic.sql", "symbolic.repaired_sql"),
    RepairSymbolicSQL('symbolic', model=LLM_MODEL),
    # SlmUnmaskAndRepair("pred_sql", model=SLM_MODEL),
    AddConcreteSql(),
    ExecuteConcreteSql(database_path),
    RepairSQL('pred_sql', model=SLM_MODEL),
    # CopyTransformer('concrete_sql', 'pred_sql'),
    CalcExecAcc(database_path),
    # AddMaskedTerms("masked_terms", model=LLM_MODEL),
    # CopyTransformer("masked_terms", "symbolic.masked_terms"),
    # SchemaLinkScore(),
    # PrivacyScore(),
    PrintResults()
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
    ExecuteConcreteSql(database_path),
    RepairSQL('pred_sql', model=REPAIR_MODEL),
    CalcExecAcc(database_path),
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

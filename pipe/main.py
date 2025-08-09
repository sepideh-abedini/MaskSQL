import asyncio
import os
import sys

from loguru import logger

from pipe.add_schema import AddSchema, AddFilteredSchema
from pipe.add_symb_schema import AddSymbolicSchema
from pipe.copy_transformer import CopyTransformer, AddGoldValues
from pipe.det_mask import AddSymbolicQuestion
from pipe.detect_entities import DetectValues
from pipe.exec_acc import ExecAccCalc
from pipe.filer_schema_links import FilterSchemaLinks
from pipe.filer_value_links import FilterValueLinks
from pipe.gen_masked_sql import GenerateSymbolicSql
from pipe.gen_sql import GenSql
from pipe.link_schema import LinkSchema
from pipe.pipeline import Pipeline
from pipe.processor.analyze import AnalyzeResults
from pipe.processor.gen_sql_eval import GenSqlEval
from pipe.processor.limit_list import LimitJson
from pipe.processor.print_results import PrintResults
from pipe.processor.schema_link_eval import SchemaLinkEval
from pipe.processor.value_link_eval import ValueLinkEval
from pipe.rank_schema import RankSchemaResd
from pipe.repair_sql import RepairSQL
from pipe.repair_symb_sql import RepairSymbolicSQL
from pipe.symb_table import AddSymbolTable
from pipe.unmask import AddConcreteSql
from pipe.value_links import LinkValues
from pipe.wrong_exec_acc import WrongExecAccOutput

LLM_MODEL = os.getenv("LLM_MODEL")
PRIVATE_MODEL = os.getenv("PRIVATE_MODEL")
SLM_MODEL = os.getenv("SLM_MODEL")
ALT_MODEL = os.getenv("ALT_MODEL")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# out_dir = "out/new/gpt"
out_dir = os.path.join("out", "o3", "0_base")

if not os.path.exists(out_dir):
    os.makedirs(out_dir, exist_ok=True)

database_path = "../../../parser/data/bird/database"
input_path = os.path.join(out_dir, "1_input.json")
tables_path = os.path.join(out_dir, "tables.json")
output_path = os.path.join(out_dir, "output.json")
eval_path = os.path.join(out_dir, "eval.json")

unmask_pipe_llm = [
    LimitJson("limit"),
    RankSchemaResd(tables_path),
    AddSchema(tables_path),
    GenSql("pred_sql", model="openai/gpt-4.1"),
    ExecAccCalc(database_path)
]

unmask_pipe_slm = [
    LimitJson("limit"),
    RankSchemaResd(tables_path),
    AddSchema(tables_path),
    GenSql("pred_sql", model=PRIVATE_MODEL),
    ExecAccCalc(database_path),
    PrintResults()
]
mask_pipe = [
    LimitJson("limit"),
    RankSchemaResd(tables_path),
    # RankSchemaItems("schema_items", tables_path),
    AddFilteredSchema(tables_path),
    AddSymbolTable(tables_path),
    DetectValues("values", model=SLM_MODEL),
    LinkValues("value_links", model=SLM_MODEL),

    CopyTransformer("value_links", "filtered_value_links"),
    # FilterValueLinks("filtered_value_links", model=SLM_MODEL),

    LinkSchema("schema_links", model=SLM_MODEL),
    CopyTransformer("schema_links", "filtered_schema_links"),
    # FilterSchemaLinks("filtered_schema_links", model=SLM_MODEL),

    # AddFilteredSymbolicSchema("symbolic", tables_path),
    AddSymbolicSchema("symbolic", tables_path),
    AddSymbolicQuestion(),
    GenerateSymbolicSql("symbolic", model=LLM_MODEL),
    RepairSymbolicSQL('symbolic', model=LLM_MODEL),
    AddConcreteSql(),
    WrongExecAccOutput(database_path),
    RepairSQL('pred_sql', model=SLM_MODEL),
    # CopyTransformer("pred_sql", "concrete_sql"),
    ExecAccCalc(database_path),
    # PrintProps(["schema", "query","symbolic.question", "pred_sql", "concrete_sql", "symbolic.sql", "question", "pre_eval.err", "eval.acc",
    #             "eval.pred_err",
    #             "pre_eval.pred_res"]),
    # AnalyzeResults()
    PrintResults()
]

value_link_eval = [
    LimitJson("limit"),
    RankSchemaResd(tables_path),
    AddFilteredSchema(tables_path),
    AddSymbolTable(tables_path),
    DetectValues("values", model=SLM_MODEL),
    LinkValues("value_links", model=SLM_MODEL),
    CopyTransformer("value_links", "filtered_value_links"),
    ValueLinkEval()
]

schema_link_eval = [
    LimitJson("limit"),
    RankSchemaResd(tables_path),
    AddFilteredSchema(tables_path),
    AddSymbolTable(tables_path),
    CopyTransformer("gold_value_links", "filtered_value_links"),
    AddGoldValues(),
    LinkSchema("schema_links", model=SLM_MODEL),
    CopyTransformer("schema_links", "filtered_schema_links"),
    SchemaLinkEval()
]

gen_sql_eval = [
    LimitJson("limit"),
    RankSchemaResd(tables_path),
    AddFilteredSchema(tables_path),
    AddSymbolTable(tables_path),
    CopyTransformer("gold_value_links", "value_links"),
    CopyTransformer("gold_value_links", "filtered_value_links"),
    AddGoldValues(),
    CopyTransformer("gold_schema_links", "schema_links"),
    CopyTransformer("gold_schema_links", "filtered_schema_links"),
    AddSymbolicSchema("symbolic", tables_path),
    AddSymbolicQuestion(),
    GenerateSymbolicSql("symbolic", model=LLM_MODEL),
    RepairSymbolicSQL('symbolic', model=LLM_MODEL),
    AddConcreteSql(),
    WrongExecAccOutput(database_path),
    GenSqlEval()
]

full_gold = [
    LimitJson("limit"),
    RankSchemaResd(tables_path),
    AddFilteredSchema(tables_path),
    AddSymbolTable(tables_path),
    CopyTransformer("gold_value_links", "value_links"),
    CopyTransformer("gold_value_links", "filtered_value_links"),
    AddGoldValues(),
    CopyTransformer("gold_schema_links", "schema_links"),
    CopyTransformer("gold_schema_links", "filtered_schema_links"),
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

    # pipeline = Pipeline(value_link_eval)
    # pipeline = Pipeline(schema_link_eval)
    # pipeline = Pipeline(gen_sql_eval)
    # pipeline = Pipeline(full_gold)
    pipeline = Pipeline(mask_pipe)

    # pipeline = Pipeline(unmask_pipe_llm)
    # pipeline = Pipeline(unmask_pipe_slm)
    out_path = await pipeline.run(input_path)
    print("LLM MODEL:", LLM_MODEL)
    print("SLM MODEL:", SLM_MODEL)
    print("ALT MODEL:", ALT_MODEL)


if __name__ == '__main__':
    asyncio.run(main())

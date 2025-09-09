import asyncio
import os
import sys

from loguru import logger

from src.pipe.add_schema import AddFilteredSchema
from src.pipe import AddSymbolicSchema
from src.pipe import AddSymbolicQuestion
from src.pipe import Pipeline
from src.pipe.processor import LimitJson
from src.pipe import RankSchemaResd
from src.pipe import AddSymbolTable

LLM_MODEL = os.getenv("LLM_MODEL")
LINK_MODEL = os.getenv("LINK_MODEL")
REPAIR_MODEL = os.getenv("REPAIR_MODEL")
PRIVATE_MODEL = os.getenv("PRIVATE_MODEL")
SLM_MODEL = os.getenv("SLM_MODEL")
ALT_MODEL = os.getenv("ALT_MODEL")
VLM_MODEL = os.getenv("VLM_MODEL")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

out_dir = os.path.join("out", "paper", "1_test")

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
    AddSymbolicSchema("symbolic", tables_path),
    AddSymbolicQuestion(),
    # DetectValues("values", model=SLM_MODEL),
    # LinkValues("value_links", model=SLM_MODEL),
    # CopyTransformer("value_links", "filtered_value_links"),
    # LinkSchema("schema_links", model=VLM_MODEL),
    # CopyTransformer("schema_links", "filtered_schema_links"),
    # AddSymbolicSchema("symbolic", tables_path),
    # AddSymbolicQuestion(),
    # GenerateSymbolicSql("symbolic", model=LLM_MODEL),
    # RepairSymbolicSQL('symbolic', model=LLM_MODEL),
    # AddConcreteSql(),
    # WrongExecAccOutput(database_path),
    # RepairSQL('pred_sql', model=SLM_MODEL),
    # ExecAccCalc(database_path),
    # AddMaskedTermsDeterministic(),
    # CopyFromPrevStage("1_input", "gold_links"),
    # Attack("attack", model=LLM_MODEL),
    # PrintResults()
]


async def main():
    try:
        logger.remove(0)
    except Exception:
        pass
    logger.add(sys.stderr, level=LOG_LEVEL, colorize=True, enqueue=True,
               format="<green>{time:HH:mm:ss}[{process.id}] | </green><level> {level}: {message}</level>")
    logger.add("llm.debug.log", level="DEBUG", filter="pipe.llm_util", format="{message}")

    pipeline = Pipeline(mask_pipe)

    out_path = await pipeline.run(input_path)
    print("LLM MODEL:", LLM_MODEL)
    print("SLM MODEL:", SLM_MODEL)


if __name__ == '__main__':
    asyncio.run(main())

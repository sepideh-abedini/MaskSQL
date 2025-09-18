import argparse
import asyncio
import os
import sys
from typing import Dict

from loguru import logger

from config import MaskSqlConfig
from src.pipe.add_schema import AddFilteredSchema
from src.pipe.attack import AddInferenceAttack
from src.pipe.det_mask import AddSymbolicQuestion
from src.pipe.detect_entities import DetectValues
from src.pipe.exec_acc import CalcExecAcc
from src.pipe.exec_conc_sql import ExecuteConcreteSql
from src.pipe.filer_schema_links import FilterSchemaLinks
from src.pipe.filer_value_links import FilterValueLinks
from src.pipe.filtered_symb_schema import AddFilteredSymbolicSchema
from src.pipe.gen_masked_sql import GenerateSymbolicSql
from src.pipe.link_schema import LinkSchema
from src.pipe.pipeline import Pipeline
from src.pipe.processor.limit_list import LimitJson
from src.pipe.processor.list_transformer import JsonListTransformer
from src.pipe.rank_schema import RankSchemaResd
from src.pipe.repair_sql import RepairSQL
from src.pipe.repair_symb_sql import RepairSymbolicSQL
from src.pipe.resdsql import AddResd
from src.pipe.results import Results
from src.pipe.symb_table import AddSymbolTable
from src.pipe.unmask import AddConcreteSql
from src.pipe.value_links import LinkValues
from src.util.json_utils import read_json
from src.util.log_utils import configure_logging


class FixFormat(JsonListTransformer):

    async def _process_row(self, row: Dict) -> Dict:
        row['query'] = row['SQL']
        return row


def create_pipeline_stages(conf: MaskSqlConfig):
    mask_pipe = [
        LimitJson("limit"),
        AddResd(conf.resd_path),
        RankSchemaResd(conf.tables_path),
        AddFilteredSchema(conf.tables_path),
        AddSymbolTable(conf.tables_path),
        DetectValues("values", model=conf.slm),
        LinkValues("value_links", model=conf.slm),
        #For Category-based!
        FilterValueLinks("filtered_value_links", model=conf.slm),
        # CopyTransformer("value_links", "filtered_value_links"),
        LinkSchema("schema_links", model=conf.slm),
        #For Category-based!
        FilterSchemaLinks("filtered_schema_links", model=conf.slm),
        AddFilteredSymbolicSchema(conf.tables_path),
        AddSymbolicQuestion(),
        GenerateSymbolicSql("symbolic", model=conf.llm),
        RepairSymbolicSQL('symbolic', model=conf.llm),
        AddConcreteSql(),
        ExecuteConcreteSql(conf.db_path),
        RepairSQL('pred_sql', model=conf.slm),
        CalcExecAcc(conf.db_path, policy=conf.policy),
        AddInferenceAttack("attack", model=conf.llm),
        Results()
    ]

    return mask_pipe

async def main():
    parser = argparse.ArgumentParser(description="MaskSQL")
    parser.add_argument("--data", type=str, required=False, help="Data directory", default="data")
    parser.add_argument("--resd", action="store_true", dest="resd", help="Use RESDSQL")
    args = parser.parse_args()
    configure_logging()
    conf = MaskSqlConfig(args.data, args.resd, "category")
    pipeline_stages = create_pipeline_stages(conf)
    pipeline = Pipeline(pipeline_stages)
    await pipeline.run(conf.input_path)




if __name__ == '__main__':
    asyncio.run(main())

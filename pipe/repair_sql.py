import json
import os

import tqdm
from loguru import logger

from pipe.detect_values_prompts.prompt_processor import PromptProcessor
from pipe.gen_sql import extract_sql
from pipe.sql_repair_prompts.v3 import REPAIR_SQL_PROMPT_V3
from pipe.sql_repair_prompts.v4 import REPAIR_SQL_PROMPT_V4
from pipe.sql_repair_prompts.v5 import REPAIR_SQL_PROMPT_V5


# from pipe.sql_repair_prompts.v4 import REPAIR_SQL_PROMPT_V4


class RepairSQL(PromptProcessor):

    def _process_output(self, row, output):
        sql = extract_sql(output)
        if sql == "SELECT":
            logger.error(f"Failed to extract sql from: {output}")
            return row['concrete_sql']
        return sql

    def _get_prompt(self, row):
        question = row['question']
        schema = row['schema']
        sql = row['concrete_sql']
        err = row['pre_eval']['err']
        pred_res = row['pre_eval']['pred_res']
        exec_res = f"Execution Result: {pred_res}, Execution Error: {err}"
        prompt = REPAIR_SQL_PROMPT_V3.format(question=question, schema=schema, sql=sql, exec_res=err)
        return prompt

    async def _process_row(self, row):
        if row['pre_eval']['acc'] == 1:
            row['pred_sql'] = row['concrete_sql']
            return row
        else:
            return await super()._process_row(row)

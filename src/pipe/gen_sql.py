import re

from loguru import logger

from src.pipe.detect_values_prompts.prompt_processor import PromptProcessor
from src.pipe.sql_gen_prompts.masked_v3 import MASKED_GEN_SQL_PROMPT_V3

DATA_DIR = "data"


def extract_sql(output):
    output = output.strip()
    output = output.strip("\"")
    sql = "SELECT"
    if output.startswith("SELECT"):
        sql = output
    elif "```sql" in output:
        res = re.findall(r"```sql([\s\S]*?)```", output)
        sql = res[0]
    elif "```" in output:
        res = re.findall(r"```([\s\S]*?)```", output)
        sql = res[0]
    elif "`" in output:
        res = re.findall(r"`([\s\S]*?)`", output)
        sql = res[0]
    else:
        logger.error(f"Failed to extract sql from output: {output}")
    sql = sql.strip()
    sql = sql.replace("\n", " ")
    return sql


class GenSql(PromptProcessor):

    def _process_output(self, row, output):
        return extract_sql(output)

    def _get_prompt(self, row):
        question = row['question']
        # schema_items = row['schema_items']
        # return GEN_SQL_PROMPT_V1.format(question=question, schema_items=schema_items)
        schema = row['schema']
        return MASKED_GEN_SQL_PROMPT_V3.format(question=question, schema=schema)

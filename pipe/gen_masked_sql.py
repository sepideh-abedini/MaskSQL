from pipe.detect_values_prompts.prompt_processor import PromptProcessor
from pipe.gen_sql import extract_sql
from pipe.sql_gen_prompts.masked_v4 import MASKED_GEN_SQL_PROMPT_V4

DATA_DIR = "data"


class GenerateSymbolicSql(PromptProcessor):

    def _process_output(self, row, output):
        masked_sql = extract_sql(output)
        return {'sql': masked_sql}

    def _get_prompt(self, row):
        symbolic_question = row['symbolic']['question']
        symbolic_schema = row['symbolic']['schema']
        return MASKED_GEN_SQL_PROMPT_V4.format(question=symbolic_question, schema=symbolic_schema)

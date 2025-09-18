from src.pipe.detect_values_prompts.prompt_processor import PromptProcessor
from src.pipe.gen_sql import extract_sql
from src.pipe.slm_sql_prompt.v1 import GENERATE_SQL_PROMPT_V1


class SlmSQL(PromptProcessor):
    def _process_output(self, row, output):
        slm_sql = extract_sql(output)
        return  slm_sql


    def _get_prompt(self, row):
        question = row['question']
        schema = row['schema']
        return GENERATE_SQL_PROMPT_V1.format(question=question, schema=schema)

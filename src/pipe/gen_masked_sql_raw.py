from src.pipe.detect_values_prompts.prompt_processor import PromptProcessor
from src.pipe.gen_sql import extract_sql
from src.pipe.sql_gen_prompts.masked_v3_raw import MASKED_GEN_SQL_RAW_PROMPT_V3

DATA_DIR = "data"


class GenerateSymbolicSqlRaw(PromptProcessor):

    def _process_output(self, row, output):
        masked_sql = extract_sql(output)
        return {'sql': masked_sql}

    def _get_prompt(self, row):
        inputs = row['symbolic']['raw']
        return MASKED_GEN_SQL_RAW_PROMPT_V3.format(inputs=inputs)

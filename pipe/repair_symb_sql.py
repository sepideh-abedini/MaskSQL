from pipe.detect_values_prompts.prompt_processor import PromptProcessor
from pipe.gen_sql import extract_sql
from pipe.symb_sql_repair_prompts.raw_v2 import REPAIR_SYMBOLIC_SQL_RAW_PROMPT_V2
from pipe.symb_sql_repair_prompts.v2 import REPAIR_SYMBOLIC_SQL_PROMPT_V2


class RepairSymbolicSQL(PromptProcessor):

    def _process_output(self, row, output):
        sql = extract_sql(output)
        return {
            "repaired_sql": sql
        }

    def _get_prompt(self, row):
        symbolic_question = row['symbolic']['question']
        symbolic_schema = row['symbolic']['schema']
        symbolic_sql = row['symbolic']['schema']
        return REPAIR_SYMBOLIC_SQL_PROMPT_V2.format(question=symbolic_question, schema=symbolic_schema,
                                                    sql=symbolic_sql)


class RepairSymbolicSQLRaw(PromptProcessor):

    def _process_output(self, row, output):
        sql = extract_sql(output)
        return {
            "repaired_sql": sql
        }

    def _get_prompt(self, row):
        symbolic_raw = row['symbolic']['raw']
        symbolic_sql = row['symbolic']['sql']
        return REPAIR_SYMBOLIC_SQL_RAW_PROMPT_V2.format(symbolic_raw=symbolic_raw, sql=symbolic_sql)

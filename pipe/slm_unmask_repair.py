from pipe.detect_values_prompts.prompt_processor import PromptProcessor
from pipe.gen_sql import extract_sql
from pipe.slm_mask_prompts.unmask_and_repair_v1 import SLM_UNMASK_AND_REPAIR_PROMPT_V1


class SlmUnmaskAndRepair(PromptProcessor):

    def _process_output(self, row, output):
        sql = extract_sql(output)
        return sql

    def _get_prompt(self, row):
        question = row['question']
        schema = row['schema']
        masked_question = row['symbolic']['question']
        masked_schema = row['symbolic']['schema']
        masked_sql = row['symbolic']['sql']
        return SLM_UNMASK_AND_REPAIR_PROMPT_V1.format(question=question, schema=schema,
                                                      masked_question=masked_question,
                                                      masked_schema=masked_schema,
                                                      masked_sql=masked_sql)

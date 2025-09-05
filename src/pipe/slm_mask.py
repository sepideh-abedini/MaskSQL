from src.pipe.detect_values_prompts.prompt_processor import PromptProcessor
from src.pipe.gen_sql import extract_sql
from src.pipe.slm_mask_prompts.mask_v1 import SLM_MASK_PROMPT_V1
from src.pipe.slm_mask_prompts.unmask_v1 import SLM_UNMASK_PROMPT_V1


class SlmMask(PromptProcessor):

    def _process_output(self, row, output):
        return {"raw": output}

    def _get_prompt(self, row):
        question = row['question']
        schema = row['schema']
        return SLM_MASK_PROMPT_V1.format(question=question, schema=schema)


class SlmUnmask(PromptProcessor):

    def _process_output(self, row, output):
        sql = extract_sql(output)
        return sql

    def _get_prompt(self, row):
        question = row['question']
        schema = row['schema']
        masked_raw = row['symbolic']['raw']
        masked_sql = row['symbolic']['sql']
        return SLM_UNMASK_PROMPT_V1.format(question=question, schema=schema, masked_raw=masked_raw,
                                           masked_sql=masked_sql)

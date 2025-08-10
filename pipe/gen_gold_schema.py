from pipe.detect_values_prompts.prompt_processor import PromptProcessor
from pipe.gold_mask.gold_mask_v1 import GOLD_MASK_V1
from pipe.gold_schema_link.v1 import GOLD_SCHEMA_LINKING_PROMPT_V1
from pipe.llm_util import extract_object


class GenGoldLinks(PromptProcessor):

    def _process_output(self, row, output):
        return extract_object(output)

    def _get_prompt(self, row):
        question = row['question']
        schema = row['schema']
        sql = row['query']
        return GOLD_SCHEMA_LINKING_PROMPT_V1.format(question=question, schema=schema, sql=sql)

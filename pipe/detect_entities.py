from typing import Dict

from pipe.detect_values_prompts.prompt_processor import PromptProcessor
from pipe.detect_values_prompts.v3 import DETECT_VALUES_PROMPT_V3
from pipe.llm_util import extract_object
from pipe.processor.list_transformer import JsonListTransformer


class DetectValues(PromptProcessor):
    def _process_output(self, row, output):
        obj = extract_object(output)
        if obj is None:
            return []
        return obj

    def _get_prompt(self, row):
        schema_items = row['schema_items']
        question = row['question']
        return DETECT_VALUES_PROMPT_V3.format(question=question, schema_items=schema_items)


class DetectValuesDummy(JsonListTransformer):
    async def _process_row(self, row: Dict) -> Dict:
        row['values'] = []
        return row

from pipe.detect_values_prompts.prompt_processor import PromptProcessor
from pipe.detect_values_prompts.v3 import DETECT_VALUES_PROMPT_V3
from pipe.llm_util import extract_json


class DetectValues(PromptProcessor):
    def _process_output(self, row, output):
        return extract_json(output)

    def _get_prompt(self, row):
        schema_items = row['schema_items']
        question = row['question']
        return DETECT_VALUES_PROMPT_V3.format(question=question, schema_items=schema_items)

from pipe.detect_values_prompts.prompt_processor import PromptProcessor
from pipe.filer_schema_links import CONCEPTS
from pipe.llm_util import extract_object
from pipe.schema_items_filter_prompts.v1 import FILTER_SCHEMA_ITEMS_PROMPT_V1


class FilterSchemaItems(PromptProcessor):
    def _process_output(self, row, output):
        return extract_object(output)

    def _get_prompt(self, row):
        schema_items = row['schema_items']
        return FILTER_SCHEMA_ITEMS_PROMPT_V1.format(concepts=CONCEPTS, schema_items=schema_items)

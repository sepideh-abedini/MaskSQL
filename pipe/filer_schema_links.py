from pipe.detect_values_prompts.prompt_processor import PromptProcessor
from pipe.llm_util import extract_json
from pipe.schema_filter_prompts.v2 import FILTER_SCHEMA_LINKS_PROMPT_V2

CONCEPTS = [
    "Person's name",
    "Location",
    "Occupation"
]


class FilterSchemaLinks(PromptProcessor):
    def _process_output(self, row, output):
        return extract_json(output)

    def _get_prompt(self, row):
        schema_links = row['schema_links']
        question = row['question']
        return FILTER_SCHEMA_LINKS_PROMPT_V2.format(concepts=CONCEPTS, question=question, schema_links=schema_links)

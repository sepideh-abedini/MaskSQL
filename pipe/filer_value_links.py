from pipe.detect_values_prompts.prompt_processor import PromptProcessor
from pipe.filer_schema_links import CONCEPTS
from pipe.llm_util import extract_object
from pipe.value_filter_prompts.v1 import VALUE_LINKS_FILTER_PROMPT_V1


class FilterValueLinks(PromptProcessor):
    def _process_output(self, row, output):
        return extract_object(output)

    def _get_prompt(self, row):
        question = row['question']
        value_links = row['value_links']
        return VALUE_LINKS_FILTER_PROMPT_V1.format(concepts=CONCEPTS, question=question, value_links=value_links)

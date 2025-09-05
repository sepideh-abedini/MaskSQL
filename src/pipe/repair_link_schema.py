from loguru import logger

from src.pipe.detect_values_prompts.prompt_processor import PromptProcessor
from src.pipe.llm_util import extract_object
from src.pipe.schema_link_prompts.repair import REPAIR_SCHEMA_LINK_PROMPT_V1


class RepairSchemaLinks(PromptProcessor):

    def _process_output(self, row, output):
        schema_links = extract_object(output)
        question = row['question']
        schema_items = row['schema_items']
        refined_links = dict()
        if isinstance(schema_links, list) or isinstance(schema_links, str):
            logger.error(f"Invalid schema links: {schema_links}")
            refined_links = dict()

        for question_term, schema_item in schema_links.items():
            if question_term not in question or schema_item not in schema_items:
                logger.error(f"Invalid schema link {question_term} -> {schema_item}")
                continue
            refined_links[question_term] = schema_item
        return refined_links

    def get_n_grams(self, text: str, n):
        words = text.split(" ")
        return [words[i:i + n] for i in range(len(words) - n + 1)]

    def _get_prompt(self, row):
        question = row['question']
        schema_items = row['schema_items']
        value_list = row['values']
        schema_links = row['schema_links']
        return REPAIR_SCHEMA_LINK_PROMPT_V1.format(schema_items=schema_items, question=question, value_List=value_list,
                                                   schema_links=schema_links)

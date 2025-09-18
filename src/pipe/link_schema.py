from loguru import logger

from src.pipe.detect_values_prompts.prompt_processor import PromptProcessor
from src.pipe.llm_util import extract_object
from src.pipe.schema_link_prompts.v4 import SCHEMA_LINK_PROMPT_V4


class LinkSchema(PromptProcessor):

    def _process_output(self, row, output):
        schema_links = extract_object(output)
        if schema_links is None:
            schema_links = dict()
        question = row['question']
        schema_items = row['schema_items']
        refined_links = dict()
        if isinstance(schema_links, list) or isinstance(schema_links, set) or isinstance(schema_links, str) or isinstance( schema_links, tuple):
            logger.error(f"Invalid schema links: {schema_links}")
            schema_links = dict()

        for question_term, schema_item in schema_links.items():
            if question_term.lower() not in question.lower():
                logger.error(f"Invalid schema link {question_term} -> {schema_item}, term not found in question")
                continue
            if schema_item.lower() not in [i.lower() for i in schema_items]:
                logger.error(f"Invalid schema link {question_term} -> {schema_item}, schema item not exists")
                continue
            refined_links[question_term] = schema_item
        return refined_links

    def _get_prompt(self, row):
        question = row['question']
        schema_items = row['schema_items']
        value_list = row['values']
        # slm_sql = row['slm_sql']
        return SCHEMA_LINK_PROMPT_V4.format(schema_items=schema_items, question=question, value_List=value_list)

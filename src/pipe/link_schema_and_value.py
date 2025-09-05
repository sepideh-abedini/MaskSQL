from loguru import logger

from src.pipe.abl_prompts.schema_value_link import SCHEMA_VALUE_LINK_PROMPT_V1
from src.pipe.detect_values_prompts.prompt_processor import PromptProcessor
from src.pipe.llm_util import extract_object


class LinkSchemaAndValue(PromptProcessor):

    def _process_output(self, row, output):
        schema_links = extract_object(output)
        if schema_links is None:
            schema_links = dict()
        question = row['question']
        schema_items = row['schema_items']
        refined_links = dict()
        if isinstance(schema_links, list) or isinstance(schema_links, str):
            logger.error(f"Invalid schema links: {schema_links}")
            refined_links = dict()

        for question_term, schema_item in schema_links.items():
            if question_term.lower() not in question.lower():
                logger.error(f"Invalid schema link {question_term} -> {schema_item}, term not found in question")
                continue
            orig_schema_item = schema_item
            if "VALUE:" in schema_item:
                schema_item = schema_item.replace('VALUE:', 'COLUMN:')
            if schema_item.lower() not in [i.lower() for i in schema_items]:
                logger.error(f"Invalid schema link {question_term} -> {orig_schema_item}, schema item not exists")
                continue
            refined_links[question_term] = orig_schema_item
        return refined_links

    def _get_prompt(self, row):
        question = row['question']
        schema_items = row['schema_items']
        value_list = row['values']
        return SCHEMA_VALUE_LINK_PROMPT_V1.format(schema_items=schema_items, question=question, value_List=value_list)

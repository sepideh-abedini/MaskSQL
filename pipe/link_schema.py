import json
import re

from loguru import logger

from pipe.detect_values_prompts.prompt_processor import PromptProcessor
from pipe.llm_util import extract_json
from pipe.schema_link_prompts.v4 import SCHEMA_LINK_PROMPT_V4


class LinkSchema(PromptProcessor):

    def _process_output(self, row, output):
        schema_links = extract_json(output)
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
        return SCHEMA_LINK_PROMPT_V4.format(schema_items=schema_items, question=question, value_List=value_list)

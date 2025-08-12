import re

from pipe.attack_prompts.add_masked_terms import ADD_MASKED_TERMS_PROMPT_V1
from pipe.detect_values_prompts.prompt_processor import PromptProcessor
from pipe.llm_util import extract_object
from pipe.processor.list_transformer import JsonListTransformer
from pipe.utils import check_str_punc


class AddMaskedTerms(PromptProcessor):

    def _process_output(self, row, output):
        output = extract_object(output)
        if output is None:
            return []
        masked_terms = list(output.keys())
        return masked_terms

    def _get_prompt(self, row):
        question = row['question']
        symbolic_question = row['symbolic']['question']
        return ADD_MASKED_TERMS_PROMPT_V1.format(question=question, masked_question=symbolic_question)

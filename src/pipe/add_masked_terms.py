from loguru import logger

from src.pipe.attack_prompts.add_masked_terms import ADD_MASKED_TERMS_PROMPT_V1
from src.pipe.detect_values_prompts.prompt_processor import PromptProcessor
from src.pipe.llm_util import extract_object


class AddMaskedTerms(PromptProcessor):

    def _process_output(self, row, output):
        output = extract_object(output)
        if output is None:
            return []
        masked_terms = list(output.keys())
        q = row['question']
        filtered_terms = []
        for m in masked_terms:
            if m.lower() in q.lower():
                filtered_terms.append(m)
            else:
                logger.error(f"{m} not in question: {q}")
        return masked_terms

    def _get_prompt(self, row):
        question = row['question']
        symbolic_question = row['symbolic']['question']
        return ADD_MASKED_TERMS_PROMPT_V1.format(question=question, masked_question=symbolic_question)

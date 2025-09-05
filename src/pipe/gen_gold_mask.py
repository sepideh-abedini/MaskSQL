from src.pipe.detect_values_prompts.prompt_processor import PromptProcessor
from src.pipe.gold_mask.gold_mask_v1 import GOLD_MASK_V1


class GenGoldMask(PromptProcessor):

    def _process_output(self, row, output):
        return output

    def _get_prompt(self, row):
        question = row['question']
        schema = row['schema']
        return GOLD_MASK_V1.format(question=question, schema=schema)

from pipe.attack_prompts.attack_raw_v1 import ATTACK_PROMPT_RAW_V1
from pipe.attack_prompts.attack_v1 import ATTACK_PROMPT_V1
from pipe.detect_values_prompts.prompt_processor import PromptProcessor


class Attack(PromptProcessor):

    def _process_output(self, row, output):
        return output

    def _get_prompt(self, row):
        symbolic_question = row['symbolic']['question']
        symbolic_schema = row['symbolic']['schema']
        return ATTACK_PROMPT_V1.format(question=symbolic_question, schema=symbolic_schema)


class AttackRaw(PromptProcessor):

    def _process_output(self, row, output):
        return output

    def _get_prompt(self, row):
        symbolic_raw = row['symbolic']['raw']
        return ATTACK_PROMPT_RAW_V1.format(symbolic_raw=symbolic_raw)

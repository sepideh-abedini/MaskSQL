from src.pipe.attack_prompts.attack_raw_v1 import ATTACK_PROMPT_RAW_V1
from src.pipe.attack_prompts.attack_v1 import ATTACK_PROMPT_V1
from src.pipe.attack_prompts.attack_v2 import ATTACK_PROMPT_V2
from src.pipe.detect_values_prompts.prompt_processor import PromptProcessor

# TODO[X]: ask to infer all tokens not only in question evidence is being ignored
class AddInferenceAttack(PromptProcessor):

    def _process_output(self, row, output):
        return output

    def _get_prompt(self, row):
        symbolic_question = row['symbolic']['question']
        symbolic_schema = row['symbolic']['schema']
        return ATTACK_PROMPT_V2.format(question=symbolic_question, schema=symbolic_schema)


class AttackRaw(PromptProcessor):

    def _process_output(self, row, output):
        return output

    def _get_prompt(self, row):
        symbolic_raw = row['symbolic']['raw']
        return ATTACK_PROMPT_RAW_V1.format(symbolic_raw=symbolic_raw)

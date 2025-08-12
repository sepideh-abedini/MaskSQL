from pipe.detect_values_prompts.prompt_processor import PromptProcessor
from pipe.gen_sql import extract_sql
from pipe.gold_mask.gold_mask_v1 import GOLD_MASK_V1
from pipe.slm_mask_prompts.mask_and_schema_link_v1 import SLM_MASK_AND_LINK_PROMPT_V1
from pipe.slm_mask_prompts.mask_v1 import SLM_MASK_PROMPT_V1
from pipe.slm_mask_prompts.unmask_v1 import SLM_UNMASK_PROMPT_V1


class SlmMaskWithSymbolTable(PromptProcessor):

    def _process_output(self, row, output):
        return {"question": output}

    def _get_prompt(self, row):
        question = row['question']
        schema = row['schema']
        symbol_table = row['symbolic']['to_symbol']
        value_links = row['value_links']
        return SLM_MASK_AND_LINK_PROMPT_V1.format(question=question, schema=schema, symbol_table=symbol_table,
                                                  value_links=value_links)

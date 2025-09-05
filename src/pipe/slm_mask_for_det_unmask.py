from src.pipe.detect_values_prompts.prompt_processor import PromptProcessor
from src.pipe.slm_mask_prompts.mask_and_schema_link_v2 import SLM_MASK_AND_LINK_PROMPT_V2


class SlmMaskWithSymbolTable(PromptProcessor):

    def _process_output(self, row, output):
        return {"question": output}

    def _get_prompt(self, row):
        question = row['question']
        schema = row['schema']
        symbol_table = row['symbolic']['to_symbol']
        value_links = row['value_links']
        return SLM_MASK_AND_LINK_PROMPT_V2.format(question=question, schema=schema, symbol_table=symbol_table,
                                                  value_links=value_links)

from pipe.detect_values_prompts.prompt_processor import PromptProcessor
from pipe.llm_util import extract_object
from pipelines.fine.add_exp import ADD_EXPLICIT_LINKS_PROMPT_V1
from pipelines.fine.repair import GOLD_SCHEMA_LINKING_REPAIR_PROMPT_V1


class RepairGoldLinks(PromptProcessor):
    def _process_output(self, row, output):
        obj = extract_object(output)
        if obj is None:
            return dict()
        return obj

    def _get_prompt(self, row):
        schema = row['schema']
        question = row['question']
        sql = row['query']
        return GOLD_SCHEMA_LINKING_REPAIR_PROMPT_V1.format(question=question, schema=schema, sql=sql)


class AddExplicitLinks(PromptProcessor):
    def _process_output(self, row, output):
        obj = extract_object(output)
        if obj is None:
            return dict()
        return obj

    def _get_prompt(self, row):
        schema = row['schema']
        question = row['question']
        sql = row['query']
        return ADD_EXPLICIT_LINKS_PROMPT_V1.format(question=question, schema=schema, sql=sql)

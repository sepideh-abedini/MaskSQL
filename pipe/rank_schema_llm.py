from pipe.detect_values_prompts.prompt_processor import PromptProcessor
from pipe.llm_util import extract_object
from pipe.rank_schema_prompts.v1 import RANK_SCHEMA_ITEMS_V1
from pipe.schema_repo import DatabaseSchemaRepo


class RankSchemaItems(PromptProcessor):
    def __init__(self, prop_name, tables_path):
        super().__init__(prop_name)
        self.schema_repo = DatabaseSchemaRepo(tables_path)

    def _process_output(self, row, output):
        return extract_object(output)

    def extract_schema_items(self, row):
        db_id = row['db_id']
        schema = self.schema_repo.dbs[db_id]
        schema_items = []

        for table_name, columns in schema.tables.items():
            schema_items.append(f"TABLE:{table_name}")
            for col_name, col_data in columns.items():
                schema_items.append(f"COLUMN:{table_name}.{col_name}")
        return schema_items

    def _get_prompt(self, row):
        question = row['question']
        schema_items = self.extract_schema_items(row)
        return RANK_SCHEMA_ITEMS_V1.format(question=question, schema_items=schema_items)

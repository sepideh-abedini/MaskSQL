from typing import List

from pipe.pipeline_stage import JsonProcessor
from pipe.schema_repo import DatabaseSchemaRepo, DatabaseSchema


class AddForeignKeys(JsonProcessor):
    def __init__(self, prop_name, tables_path):
        super().__init__(prop_name, force=True)
        self.schema_repo = DatabaseSchemaRepo(tables_path)

    async def _process_row(self, row):
        fks = []
        schema = self.schema_repo.dbs[row['db_id']]
        for table_name, table_columns in schema.tables.items():
            for col_name, col_data in table_columns.items():
                if isinstance(col_data, dict) and 'foreign_key' in col_data:
                    fks.append(f"{table_name}.{col_name}={col_data['foreign_key']}")
        return fks

from src.pipe.processor.list_transformer import JsonListTransformer
from src.pipe.schema_repo import DatabaseSchemaRepo


class RankSchemaResd(JsonListTransformer):
    def __init__(self, tables_path):
        super().__init__(force=True)
        self.schema_repo = DatabaseSchemaRepo(tables_path)

    async def _process_row(self, row):
        schema_items = row['tc_original']
        schema = self.schema_repo.dbs[row['db_id']]
        refined_schema_items = []
        for item in schema_items:
            parts = item.split(".")
            table_name = parts[0]
            table_name = f"[{table_name}]"
            column_name = parts[1]
            column_name = f"[{column_name}]"
            if table_name not in schema.tables:
                raise Exception(f"Table {table_name} not found in schema")
            table = schema.tables[table_name]
            if column_name not in table and column_name != "[*]":
                raise Exception(f"Column {column_name} not found in table {table_name}")
            table_item = f"TABLE:{table_name}"
            if table_item not in refined_schema_items:
                refined_schema_items.append(f"TABLE:{table_name}")
            refined_schema_items.append(f"COLUMN:{table_name}.{column_name}")
        row['schema_items'] = refined_schema_items
        return row

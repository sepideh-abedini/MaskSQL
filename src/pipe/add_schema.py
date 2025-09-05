from typing import List

from src.pipe.processor.list_transformer import JsonListTransformer
from src.pipe.schema_repo import DatabaseSchemaRepo, DatabaseSchema


def filter_schema(schema: DatabaseSchema, schema_items: List[str]):
    columns = set()
    for item in schema_items:
        item_ref = item.split(":")[1]
        if "[*]" in item_ref:
            continue
        if item.split(":")[0] == "COLUMN":
            columns.add(item_ref)

    for col_ref in list(columns):
        table_name = col_ref.split(".")[0]
        col_name = col_ref.split(".")[1]
        col_data = schema.tables[table_name][col_name]
        if isinstance(col_data, dict) and "foreign_key" in col_data:
            fk_ref = col_data["foreign_key"]
            columns.add(fk_ref)

    filtered_schema = DatabaseSchema()
    for table_name, table_columns in schema.tables.items():
        filtered_table_columns = dict()
        for col_name, col_data in table_columns.items():
            if f"{table_name}.{col_name}" in columns:
                filtered_table_columns[col_name] = col_data
        if len(filtered_table_columns) > 0:
            filtered_schema.tables[table_name] = filtered_table_columns
    return filtered_schema


class AddSchema(JsonListTransformer):

    def __init__(self, tables_path):
        super().__init__(force=True)
        self.schema_repo = DatabaseSchemaRepo(tables_path)

    async def _process_row(self, row):
        schema = self.schema_repo.dbs[row['db_id']]
        row['schema'] = schema.to_yaml()
        return row


class AddFilteredSchema(JsonListTransformer):

    def __init__(self, tables_path):
        super().__init__(force=True)
        self.schema_repo = DatabaseSchemaRepo(tables_path)

    async def _process_row(self, row):
        schema = self.schema_repo.dbs[row['db_id']]
        schema_items = row['schema_items']
        filtered_schema = filter_schema(schema, schema_items)
        row['schema'] = filtered_schema.to_yaml()
        return row


class AddSchemaItems(JsonListTransformer):
    def __init__(self, tables_path):
        super().__init__(force=True)
        self.schema_repo = DatabaseSchemaRepo(tables_path)

    async def _process_row(self, row):
        schema = self.schema_repo.dbs[row['db_id']]
        schema_items = []
        for table, columns in schema.tables.items():
            schema_items.append(f"TABLE:{table}")
            for col, col_data in columns.items():
                schema_items.append(f"COLUMN:{table}.{col}")
            schema_items.append(f"COLUMN:{table}.[*]")
        row['schema_items'] = schema_items
        return row

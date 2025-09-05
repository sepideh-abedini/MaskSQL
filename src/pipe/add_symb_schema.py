from typing import Dict, Union

from src.pipe.processor.list_transformer import JsonListTransformer
from src.pipe.schema_repo import DatabaseSchemaRepo, DatabaseSchema


class AddSymbolicSchema(JsonListTransformer):

    def __init__(self, tables_path):
        super().__init__()
        self.schema_repo = DatabaseSchemaRepo(tables_path)

    async def _process_row(self, row):

        schema = DatabaseSchema.from_yaml(row['schema'])
        symbol_table = row['symbolic']['to_symbol']

        symbolic_schema = self.get_symb_schema(schema, symbol_table)

        reverse_dict = self.get_reverse_dict(schema, symbol_table)
        row['symbolic']['schema'] = symbolic_schema.to_yaml()
        row['symbolic']['reverse_dict'] = reverse_dict
        return row

    def get_col_symbol(self, table_name: str, col_name: str, symbol_table: Dict[str, str]) -> str:
        col_ref = f"{table_name}.{col_name}"
        return symbol_table[col_ref]

    def get_table_symbol(self, table_name: str, symbol_table: Dict[str, str]) -> str:
        return symbol_table[table_name]

    def get_symbolic_col_data(self, col_data: Union[str, Dict[str, str]], symbol_table: Dict[str, str]) -> str:
        if isinstance(col_data, dict) and "foreign_key" in col_data:
            symbolic_col_data = col_data.copy()
            foreign_col_ref = symbolic_col_data['foreign_key']
            table_name = foreign_col_ref.split(".")[0]
            table_symbol = self.get_table_symbol(table_name, symbol_table)
            column_name = foreign_col_ref.split(".")[1]
            column_symbol = self.get_col_symbol(table_name, column_name, symbol_table)
            symbolic_col_data['foreign_key'] = f"{table_symbol}.{column_symbol}"
        else:
            symbolic_col_data = col_data
        return symbolic_col_data

    def get_symb_schema(self, schema: DatabaseSchema, symbol_table: Dict[str, str]) -> DatabaseSchema:
        symbolic_schema = DatabaseSchema()

        for table_name, columns in list(schema.tables.items()):
            symbolic_columns = dict()
            for col_name, col_data in columns.items():
                col_symbol = self.get_col_symbol(table_name, col_name, symbol_table)
                symbolic_col_data = self.get_symbolic_col_data(col_data, symbol_table)
                symbolic_columns[col_symbol] = symbolic_col_data
            table_symbol = self.get_table_symbol(table_name, symbol_table)
            symbolic_schema.tables[table_symbol] = symbolic_columns
        return symbolic_schema

    def get_reverse_dict(self, schema: DatabaseSchema, symbol_table: Dict[str, str]) -> Dict[str, str]:
        reverse_dict = dict()
        for table_name, columns in list(schema.tables.items()):
            table_symbol = symbol_table[table_name]
            reverse_dict[table_symbol] = table_name
            for col_name, col_data in columns.items():
                col_ref = f"{table_name}.{col_name}"
                col_symbol = symbol_table[col_ref]
                reverse_dict[f"{table_symbol}.{col_symbol}"] = col_ref
                reverse_dict[col_symbol] = col_ref
        return reverse_dict

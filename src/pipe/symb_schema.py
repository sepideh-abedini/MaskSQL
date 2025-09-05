from src.pipe.schema_repo import DatabaseSchemaRepo, DatabaseSchema
from ut.json_utils import JsonProcessor


class SymbSchema(JsonProcessor):

    def __init__(self, prop_name, input_file, output_file, tables_path):
        super().__init__(prop_name, input_file, output_file, True)
        self.schema_repo = DatabaseSchemaRepo(tables_path)

    async def _process_row(self, row):
        schema = self.schema_repo.dbs[row['db_id']]
        symbol_table = row['symbol_table']['to_symbol']
        symbolic_schema = DatabaseSchema()
        for table_name, columns in list(schema.tables.items()):
            symbolic_columns = dict()
            table_symbol = symbol_table[table_name]
            for col_name, col_data in columns.items():
                col_ref = f"{table_name}.{col_name}"
                col_symbol = symbol_table[col_ref]
                if isinstance(col_data, dict):
                    symbolic_col_data = col_data.copy()
                    foreign_key_symbol = symbol_table[col_data['foreign_key']]
                    symbolic_col_data['foreign_key'] = foreign_key_symbol
                else:
                    symbolic_col_data = col_data
                symbolic_columns[col_symbol] = symbolic_col_data
            symbolic_schema.tables[table_symbol] = symbolic_columns
        return symbolic_schema.to_yaml()

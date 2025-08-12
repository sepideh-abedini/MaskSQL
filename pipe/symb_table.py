from pipe.add_schema import filter_schema
from pipe.processor.list_transformer import JsonListTransformer
from pipe.schema_repo import DatabaseSchemaRepo, DatabaseSchema


class AddSymbolTable(JsonListTransformer):

    def __init__(self, tables_path):
        super().__init__(True)
        self.schema_repo = DatabaseSchemaRepo(tables_path)

    def table_symbol(self, idx):
        return f"[T{idx}]"

    def col_symbol(self, idx):
        return f"[C{idx}]"

    async def _process_row(self, row):
        schema = DatabaseSchema.from_yaml(row['schema'])
        tid = 1
        cid = 1
        symbol_table = dict()
        rev_table = dict()
        for table_name, columns in schema.tables.items():
            table_symbol = self.table_symbol(tid)
            tid += 1
            symbol_table[table_symbol] = table_name
            rev_table[table_name] = table_symbol
            for col_name in columns.keys():
                col_ref = f"{table_name}.{col_name}"
                col_symbol = f"{self.col_symbol(cid)}"
                cid += 1
                symbol_table[col_symbol] = col_ref
                rev_table[col_ref] = col_symbol
        row['symbolic'] = {
            "to_name": symbol_table,
            "to_symbol": rev_table
        }
        return row


class AddValueSymbolTable(JsonListTransformer):

    def __init__(self, tables_path):
        super().__init__(True)
        self.schema_repo = DatabaseSchemaRepo(tables_path)

    async def _process_row(self, row):
        vid = 1
        value_links = row['value_links']
        symbol_table = row['symbolic']['to_symbol']
        to_value = dict()
        for value in value_links.keys():
            symbol = f"[V{vid}]"
            symbol_table[value] = symbol
            to_value[symbol] = value
            vid += 1
        row['symbolic']['to_symbol'] = symbol_table
        row['symbolic']['to_value'] = to_value
        return row

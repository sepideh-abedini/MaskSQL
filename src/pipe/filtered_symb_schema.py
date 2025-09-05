from typing import Set, Dict, Tuple, Union

from loguru import logger

from src.pipe.processor.list_transformer import JsonListTransformer
from src.pipe.schema_repo import DatabaseSchemaRepo, DatabaseSchema


class AddFilteredSymbolicSchema(JsonListTransformer):

    def __init__(self, tables_path):
        super().__init__()
        self.schema_repo = DatabaseSchemaRepo(tables_path)

    async def _process_row(self, row):
        tables, col_refs = self.get_items_to_symbolize(row)

        schema = DatabaseSchema.from_yaml(row['schema'])
        symbol_table = row['symbolic']['to_symbol']

        symbolic_schema = self.get_symb_schema(schema, symbol_table, tables, col_refs)

        reverse_dict = self.get_reverse_dict(tables, col_refs, symbol_table)

        row['symbolic']['schema'] = symbolic_schema.to_yaml()
        row['symbolic']['reverse_dict'] = reverse_dict

        return row

    def get_col_symbol(self, table_name: str, col_name: str, col_refs: Set[str], symbol_table: Dict[str, str]) -> str:
        col_ref = f"{table_name}.{col_name}"
        if col_ref in col_refs:
            return symbol_table[col_ref]
        return col_name

    def get_table_symbol(self, table_name: str, tables: Set[str], symbol_table: Dict[str, str]) -> str:
        if table_name in tables:
            return symbol_table[table_name]
        return table_name

    def get_symbolic_col_data(self, col_data: Union[str, Dict[str, str]], tables: Set[str], col_refs: Set[str],
                              symbol_table: Dict[str, str]) -> str:
        if isinstance(col_data, dict) and "foreign_key" in col_data:
            symbolic_col_data = col_data.copy()
            foreign_col_ref = symbolic_col_data['foreign_key']
            table_name = foreign_col_ref.split(".")[0]
            table_symbol = self.get_table_symbol(table_name, tables, symbol_table)
            column_name = foreign_col_ref.split(".")[1]
            column_symbol = self.get_col_symbol(table_name, column_name, col_refs, symbol_table)
            symbolic_col_data['foreign_key'] = f"{table_symbol}.{column_symbol}"
        else:
            symbolic_col_data = col_data
        return symbolic_col_data

    def get_items_to_symbolize(self, row) -> Tuple[Set[str], Set[str]]:
        schema_items = row['filtered_schema_links']
        value_links = row['filtered_value_links']
        tables = set()
        columns = set()

        for item in schema_items.values():
            if not item or item.strip() == "{}":
                continue
            if ":" not in item:
                logger.error(f"Invalid schema item: {item}")
                continue
            item_type = item.split(":")[0]
            item_ref = item.split(":")[1]
            if item_type.startswith("TABLE"):
                tables.add(item_ref)
            if item_type.startswith("COLUMN"):
                table_name = item_ref.split(".")[0]
                tables.add(table_name)
                columns.add(item_ref)

        if isinstance(value_links, dict):
            for item in value_links.values():
                columns.add(item)
        else:
            logger.error(f"Invalid value links: {value_links}")
        return tables, columns

    def get_symb_schema(self, schema: DatabaseSchema, symbol_table: Dict[str, str],
                        tables: Set[str], col_refs: Set[str]) -> DatabaseSchema:
        symbolic_schema = DatabaseSchema()

        for table_name, columns in list(schema.tables.items()):
            symbolic_columns = dict()
            for col_name, col_data in columns.items():
                col_symbol = self.get_col_symbol(table_name, col_name, col_refs, symbol_table)
                symbolic_col_data = self.get_symbolic_col_data(col_data, tables, col_refs, symbol_table)
                symbolic_columns[col_symbol] = symbolic_col_data
            table_symbol = self.get_table_symbol(table_name, tables, symbol_table)
            symbolic_schema.tables[table_symbol] = symbolic_columns
        return symbolic_schema

    def get_reverse_dict(self, tables: Set[str], col_refs: Set[str], symbol_table: Dict[str, str]) -> Dict[str, str]:
        reverse_dict = dict()
        for table in tables:
            if table not in symbol_table:
                logger.error(f"Table {table} not found in symbol table: {symbol_table.keys()}")
                continue
            table_symbol = symbol_table[table]
            reverse_dict[table_symbol] = table

        for col_ref in col_refs:
            if "." not in col_ref:
                logger.error(f"Invalid col ref: {col_ref}")
                continue
            if col_ref not in symbol_table:
                logger.error(f"Invalid col ref: {col_ref}")
                continue
            table = col_ref.split(".")[0]

            table_symbol = symbol_table[table]
            col_symbol = symbol_table[col_ref]

            reverse_dict[col_symbol] = col_ref
            reverse_dict[f'{table_symbol}.{col_symbol}'] = col_ref
        return reverse_dict

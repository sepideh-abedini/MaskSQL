from typing import Dict, Union, List

from loguru import logger

from pipe.processor.list_transformer import JsonListTransformer
from pipe.utils import replace_str


class MaskWithGoldData(JsonListTransformer):
    def __init__(self):
        super().__init__(force=True)
        self.v_count = 0

    def get_symbol(self, schema_items: Union[List[str], str], symbol_table: Dict[str, str]) -> str:
        if not isinstance(schema_items, list):
            schema_items = [schema_items]
        symbols = []
        for schema_item in schema_items:
            if "VALUE:" in schema_item:
                self.v_count += 1
                return f"[V{self.v_count}]"
            schema_item_parts = schema_item.split(":")
            schema_item = schema_item_parts[1]
            symbol = symbol_table.get(schema_item)
            symbols.append(symbol)
        return ",".join(symbols)

    def symbolize_term(self, question: str, question_term: str, schema_items: str,
                       symbol_table: Dict[str, str]) -> str:
        symbol = self.get_symbol(schema_items, symbol_table)
        symbolic_question = replace_str(question, question_term, symbol)
        return symbolic_question

    def symbolize_value(self, question: str, question_term: str, column_ref: str,
                        updated_schema_links: Dict[str, str],
                        filtered_value_links: Dict[str, str],
                        symbol_table: Dict[str, str]) -> str:
        value_symbol = f"[V{self.vid}]"
        if column_ref in filtered_value_links.values() or f"COLUMN:{column_ref}" in updated_schema_links.values():
            column_symbol = symbol_table[column_ref]
        else:
            column_symbol = column_ref
        self.vid += 1
        evidence = f"{value_symbol} is a value of the column {column_symbol}"
        self.value_dict[value_symbol] = question_term
        symbolic_question = replace_str(question, question_term, value_symbol)
        symbolic_question = f"{symbolic_question}; {evidence}"
        return symbolic_question

    def add_tables_of_columns(self, schema_links: Dict[str, str], filtered_schema_links: Dict[str, str]):
        updated_schema_links = filtered_schema_links.copy()
        tables = set()
        for schema_items in filtered_schema_links.values():
            if schema_items is None:
                logger.error(f"Invalid schema item: {schema_items}")
                continue
            if not isinstance(schema_items, list):
                schema_items = [schema_items]
            for schema_item in schema_items:
                if schema_item.startswith("COLUMN"):
                    col_ref = schema_item.split(":")[1]
                    table_name = col_ref.split(".")[0]
                    tables.add(table_name)

        for question_term, schema_items in schema_links.items():
            if not isinstance(schema_items, list):
                schema_items = [schema_items]
            for schema_item in schema_items:
                if schema_item.startswith("TABLE"):
                    assert len(schema_items) == 1
                    table_name = schema_item.split(":")[1]
                    if table_name in tables:
                        updated_schema_links[question_term] = schema_item
        return updated_schema_links

    async def _process_row(self, row):
        self.vid = 1
        self.value_dict = dict()
        schema_links = row['annotated_links']
        question = row['question']
        symbol_table = row['symbolic']['to_symbol']
        masked_terms = []

        symbolic_question = question
        masked = 0

        sorted_schema_terms = sorted(schema_links.keys(), key=len, reverse=True)

        for question_term in sorted_schema_terms:
            schema_items = schema_links[question_term]
            try:
                symbolic_question = self.symbolize_term(symbolic_question, question_term, schema_items, symbol_table)
                masked_terms.append(question_term)
                masked += 1
            except Exception as e:
                logger.error(f"Failed to mask {question_term}:{schema_items}, error={e} ")

        row['symbolic'].update(
            {
                "question": symbolic_question,
                "to_value": self.value_dict,
                "masked": masked,
                "masked_terms": masked_terms
            }
        )
        return row

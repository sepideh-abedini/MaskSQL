from difflib import SequenceMatcher
from typing import Dict, List, Set, Tuple, FrozenSet
from loguru import logger


def str_similarity(s1, s2):
    return SequenceMatcher(None, s1.lower(), s2.lower()).ratio()


class DatabaseSchemaSqlyzr:
    tables: Dict[str, Dict[str, str]]  # {table_name -> {col_name -> col_type}}
    foreign_keys: Set[FrozenSet[Tuple[str, str]]]

    def __init__(self):
        self.tables = {}
        self.foreign_keys = set()

    def find_most_similar_column(self, table_name, col_name, cand_cols: Set[str]):
        if table_name not in self.tables:
            logger.debug(f"Table not found: {table_name}")
            return None
        table = self.tables[table_name]
        max_sim = 0
        best_col = None
        for col in cand_cols:
            sim = str_similarity(col, col_name)
            if sim >= max_sim:
                max_sim = sim
                best_col = col
        if max_sim > 0.5:
            return best_col
        for col in table:
            sim = str_similarity(col, col_name)
            if sim >= max_sim:
                max_sim = sim
                best_col = col
        if max_sim > 0.5:
            return best_col
        return None

    def get_col_type(self, table_name, col_name) -> str:
        if table_name not in self.tables:
            logger.debug(f"Table not found: {table_name}")
            return 'NA'
        table = self.tables[table_name]
        if col_name in table:
            return table[col_name]
        else:
            logger.debug(f"Column not found: {col_name}")
            return 'NA'

    def get_table_name(self, col_name: str, candidate_tables: List[str]) -> str:
        """Find the table that has a column with the given name by only searching
        in tables that are given as candidate_tables."""
        matched_tables = []
        for table in candidate_tables:
            if table not in self.tables:
                logger.debug(f"Candidate table not found: {table}, Available tables: {self.tables.keys()}")
                return "NA"
            if col_name in self.tables[table]:
                matched_tables.append(table)
        if len(matched_tables) == 1:
            return matched_tables[0]
        if len(matched_tables) == 0:
            logger.debug(f"Column not found in candidate tables: {col_name}, {candidate_tables}")
        for table in self.tables:
            if col_name in self.tables[table]:
                matched_tables.append(table)
        if len(matched_tables) == 1:
            return matched_tables[0]
        if len(matched_tables) == 0:
            logger.debug(f"Column not found in candidate tables: {col_name}, {candidate_tables}")
            return "NA"
        if len(matched_tables) > 1:
            logger.debug(f"Ambiguous column name: {col_name}, matched tables: {matched_tables}")
            return matched_tables[0]

    def __str__(self):
        res = "\nTables: \n"
        for table, columns in self.tables.items():
            res += f"\tTable Name: {table}\n"
            res += f"\t\tColumns:\n"
            for col, col_type in columns.items():
                res += f"\t\t\tColumn Name: {col}, Column type: {col_type}\n"
        return res

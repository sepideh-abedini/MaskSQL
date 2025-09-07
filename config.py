import os
from dataclasses import dataclass


@dataclass
class MaskSqlConfig:
    data_dir: str
    resd: bool
    slm: str = os.environ['SLM_MODEL']
    llm: str = os.environ['LLM_MODEL']
    __input_file: str = "1_input.json"
    __db_dir: str = "databases"
    __tables_file: str = "tables.json"
    __resd_file: str = "resd_output.json"

    def get_abs_path(self, rel_path):
        return os.path.join(self.data_dir, rel_path)

    @property
    def input_path(self):
        return self.get_abs_path(self.__input_file)

    @property
    def tables_path(self):
        return self.get_abs_path(self.__tables_file)

    @property
    def resd_path(self):
        return self.get_abs_path(self.__resd_file)

    @property
    def db_path(self):
        return self.get_abs_path(self.__db_dir)

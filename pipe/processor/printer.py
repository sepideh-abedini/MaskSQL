import json
from abc import ABC, abstractmethod
from typing import Dict

from pipe.async_utils import apply_async
from pipe.processor.list_processor import JsonListProcessor


class DataPrinter(JsonListProcessor, ABC):

    async def run(self, input_file):
        output_file = input_file
        await super().run(input_file)
        return output_file


class CustomPrinter(DataPrinter):
    async def _process_row(self, row: Dict) -> Dict:
        print("-" * 10)
        print("Question:", row['question'])
        print("Masked:", row['symbolic']['question'])
        # print("REP:", row['repaired_schema_links'])
        print("-" * 10)
        return row

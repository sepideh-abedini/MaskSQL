import json
import os
from itertools import count
from typing import Dict

# from src.pipe.processor.list_processor import JsonListProcessor
from src.pipe.processor.list_transformer import JsonListTransformer



class ResdItemCount(JsonListTransformer):
    def __init__(self):
        super().__init__()
        self.total_tables = 0

    async def _process_row(self, row: Dict) -> Dict:
        count = 0
        for items in row["schema_items"]:
            if items.startswith("TABLE"):
                count +=1
        self.total_tables += count
        return row

    def _post_run(self):
        print(f"After processing all rows total tables = {self.total_tables}")



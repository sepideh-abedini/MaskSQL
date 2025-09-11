from typing import Dict

from src.pipe.processor.list_transformer import JsonListTransformer
from src.util.json_utils import read_json


class AddResd(JsonListTransformer):
    def __init__(self, resd_path):
        super().__init__()
        self.resd = read_json(resd_path)

    async def _process_row(self, row: Dict) -> Dict:
        for r in self.resd:
            if r['question_id'] == row['question_id']:
                row['tc_original'] = r['tc_original']
                return row
        raise RuntimeError(f"Row with qid = {row['question_id']} not found")

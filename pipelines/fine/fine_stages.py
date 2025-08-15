import json
from typing import Dict

from pipe.processor.printer import DataPrinter


class Inspector(DataPrinter):
    def __init__(self):
        self.count = 0

    async def _process_row(self, row: Dict) -> Dict:
        question = row['question']
        sql = row['query']
        masked = row['symbolic']['question']
        gold_links = row['gold_links']
        repaired_links = row['repaired_gold_links']
        # revised_links = row['gold_links']
        pred_links = row['schema_links']
        acc = row['eval']['acc']
        schema = row['schema']
        self.count += 1
        if 'question_id' in row:
            return row
        print("-" * 100)
        print(f"#{self.count}")
        print("SQL:", sql)
        print("Question:", question)
        print("Links   :\n", json.dumps(gold_links, indent=4))
        print("Repaired:\n", json.dumps(repaired_links, indent=4))
        return row

from pipe.processor.list_processor import JsonListProcessor
import spacy

from pipe.processor.printer import DataPrinter


def similar(a: str, b: str) -> bool:
    a = a.strip().lower()
    b = b.strip().lower()
    if a == b:
        return True
    return False


class SchemaLinkScore(DataPrinter):
    def __init__(self):
        super().__init__()
        self.sum = 0
        self.score = 0
        self.total = 0
        self.total_pred = 0
        self.count = 0

    def _post_run(self):
        print(f"Total Links: {self.total_pred}")
        print(f"Masks: {self.sum}/{self.total}")
        print(f"Mask Score: {self.score / self.count}")

    async def _process_row(self, row):
        gold_links = row['gold_links']
        pred_links = row['filtered_schema_links']
        pred_values = row['filtered_value_links']
        pred_keys = list(pred_links.keys()) + list(pred_values.keys())

        covered = 0
        not_found = []
        for q_term, schema_item in gold_links.items():
            for p_term in pred_keys:
                if similar(q_term, p_term):
                    covered += 1
                else:
                    not_found.append(q_term)

        num_gold_keys = len(gold_links.keys())
        score = covered / num_gold_keys
        self.sum += covered
        self.total += num_gold_keys
        self.score += score
        self.total_pred += len(pred_keys)
        self.count += 1
        return row

        print("-" * 100)
        print(f"Score: {covered}/{num_gold_keys} = {score}")
        print("GOLD:\n", gold_links)
        print("PRED:")
        print(pred_links)
        print(pred_values)
        print("Not Found:")
        print(not_found)
        print("-" * 100)

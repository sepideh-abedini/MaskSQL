import pandas as pd

from src.pipe.processor.list_processor import JsonListProcessor


class ValueLinkEval(JsonListProcessor):
    def __init__(self):
        super().__init__()
        self.scores = []

    def _post_run(self):
        df = pd.DataFrame(self.scores)
        df['bin'] = (df['score'] == df['total']).astype(int)
        avg = (df['score'].sum() / df['total'].sum())
        overall_avg = (df['score'] / df['total']).mean()
        bin_avg = df['bin'].mean()
        print(f"Score: {df['score'].sum()}/{df['total'].sum()}")
        print(f"AVG Score: {avg}")
        print(f"Overall AVG Score: {overall_avg}")
        print(f"Binary Score: {bin_avg}")

    async def _process_row(self, row):
        gold = row['gold_value_links']
        pred = row['filtered_value_links']
        print("##############################")
        print(f"GOLD: {gold}")
        print("------------------------------")
        print(f"PRED: {pred}")
        print("##############################")
        score = 0
        total = 0
        for gk, gv in gold.items():
            total += 1
            if gk in pred:
                if pred[gk] == gv:
                    score += 1

        self.scores.append({
            'score': score,
            'total': total
        })

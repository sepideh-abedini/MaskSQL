from typing import Dict

import pandas as pd

from src.pipe.processor.list_transformer import JsonListTransformer


class Results(JsonListTransformer):

    def __init__(self):
        super().__init__()
        self.stat_rows = []
        self.ea = 0
        self.pre_ea = 0
        self.time = 0
        self.toks = 0
        self.count = 0
        self.ri_score = 0
        self.total_leaks = 0
        self.total_masks = 0
        self.a_count = 0
        self.recall_scores = []

    def _post_run(self):
        df = pd.DataFrame(self.stat_rows)
        print(df.mean())
        # print("Count: ", self.count)
        # if len(self.recall_scores) > 0:
        #     print(len(self.recall_scores))
        #     print(len(self.recall_scores))
        #     print(sum(self.recall_scores) / len(self.recall_scores))

    async def _process_row(self, row: Dict) -> Dict:
        stat = dict()
        if 'eval' in row:
            ea = row['eval']['acc']
            stat['EA'] = ea
        if 'total_latency' in row:
            stat['Tokens'] = row['total_toks']
            stat['Latency'] = row['total_latency']
        if 'pre_eval' in row:
            stat['pre_acc'] = row['pre_eval']['acc']
        self.count += 1
        self.stat_rows.append(stat)
        if 'attack' in row and 'annotated_links' in row:
            masked_terms = row['symbolic']['masked_terms']
            attack = row['attack']
            a_links = row['annotated_links']
            # a_links = row['filt_anon_links']

            ri_terms = 0
            num_masks = len(masked_terms)
            for term in masked_terms:
                if term.lower() in attack.lower():
                    ri_terms += 1
            if num_masks > 0:
                ris = ri_terms / num_masks
            else:
                ris = 0
            stat['ris'] = 1 - ris

            mask_covering = 0
            a_masks = len(a_links)
            for a_term, a_item in a_links.items():
                a_term = a_term.lower()
                for term in masked_terms:
                    term = term.lower()
                    if a_term in term:
                        mask_covering += 1
                        break
            if a_masks == 0:
                mcs = 1
            else:
                mcs = mask_covering / a_masks
                self.recall_scores.append(mcs)
            stat['mcs'] = mcs
            stat['a_masks'] = a_masks

        return row


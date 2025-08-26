import asyncio
import os
import sys
from typing import Dict

import pandas as pd
from loguru import logger

from pipe.copy_transformer import CopyTransformer
from pipe.pipeline import Pipeline
from pipe.processor.limit_list import FilterList
from pipe.processor.list_transformer import JsonListTransformer
from pipe.sqlite_facade import SqliteFacade
from src.cat.catter import Catter
from ut.json_utils import read_json

out_dir = os.path.join("out", "latest_msc")

if not os.path.exists(out_dir):
    os.makedirs(out_dir, exist_ok=True)

database_path = "../parser/data/bird/database"
input_path = os.path.join(out_dir, "1_input.json")
tables_path = os.path.join(out_dir, "tables.json")


class AddPred(JsonListTransformer):
    def __init__(self):
        super().__init__()
        rows = read_json(os.path.join(out_dir, "msc_out.json"))
        self.preds = dict()
        for row in rows:
            idx = row['idx']
            [_, idx] = idx.split("_")
            idx = int(idx)
            self.preds[idx] = row

    async def _process_row(self, row: Dict) -> Dict:
        idx = row['question_id']
        pred_row = self.preds[idx]
        row['total_latency'] = 0
        row['total_toks'] = 0
        row['gold'] = row['SQL']
        row['pred'] = pred_row['sql_pred']
        return row


class EvalPred(JsonListTransformer):
    def __init__(self, database_dir):
        super().__init__(False)
        self.dbf = SqliteFacade(database_dir)
        self.count = 0

    async def _process_row(self, row):
        gold = row['gold']
        pred = row['pred']
        db_id = row['db_id']
        self.count += 1
        try:
            gold_res, _ = self.dbf.exec_query_sync(db_id, gold)
            pred_res, err = self.dbf.exec_query_sync(db_id, pred)
            if gold_res == pred_res:
                acc = 1
            else:
                acc = 0
            row['eval'] = {
                "acc": acc,
                "gold": gold_res,
                "pred": pred_res,
                "pred_err": err
            }
            # print(f"SQL Executed: {self.count}")
            return row
        except Exception as e:
            print(e)
            raise e


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

    def _post_run(self):
        df = pd.DataFrame(self.stat_rows)
        print(df.mean())
        print("Count: ", self.count)

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

            ri_terms = 0
            num_masks = len(masked_terms)
            for term in masked_terms:
                if term.lower() in attack.lower():
                    ri_terms += 1
            if num_masks > 0:
                ris = ri_terms / num_masks
            else:
                ris = 0
            stat['ris'] = ris

            mask_covering = 0
            a_masks = len(a_links)
            for a_term, a_item in a_links.items():
                a_term = a_term.lower()
                for term in masked_terms:
                    term = term.lower()
                    if a_term in term:
                        mask_covering += 1
                        break
            mcs = mask_covering / a_masks
            stat['mcs'] = mcs

        return row


class AssignCat(JsonListTransformer):
    def __init__(self):
        super().__init__(force=False)
        self.catter = Catter()

    async def _process_row(self, row):
        sql = row['gold']
        cat = self.catter.get_category(sql)
        sub = self.catter.get_sub_category(sql)
        row['cat'] = cat.name
        row['sub'] = sub.name
        return row


class Charter(JsonListTransformer):
    def __init__(self):
        super().__init__()
        self.rows = []

    def _post_run(self):
        df = pd.DataFrame(self.rows)
        df['count'] = 1
        df = df[['count', 'cat', 'ea']]
        res = df.groupby(['cat', 'ea']).sum()
        print(res.reset_index())
        # cat_order = natsorted(df["cat"].unique())
        # plt.figure(figsize=(5, 5))
        # sns.countplot(df, x="cat", order=cat_order)
        # plt.show()

    async def _process_row(self, row: Dict) -> Dict:
        self.rows.append(row)
        return row


class CollectRows(JsonListTransformer):
    def __init__(self):
        super().__init__()
        self.collected = {
            'c4': [[], []],
            'c5': [[], []],
            'c6': [[], []]
        }
        self.desired_counts = {
            'c4': [100, 63],
            'c5': [33, 16],
            'c6': [44, 44]
        }

    async def _process_row(self, row: Dict) -> Dict:
        cat = row['cat']
        ea = int(row['ea'])
        row['selected'] = False
        if cat not in self.desired_counts:
            return row
        collection = self.collected[cat][ea]
        desired_count = self.desired_counts[cat][ea]
        if len(collection) < desired_count:
            collection.append(row)
            row['selected'] = True

        return row


async def main():
    pipe = [
        AddPred(),
        EvalPred(database_path),
        # AssignCat(),
        # CollectRows(),
        # FilterList(lambda r: r['eval']['acc'] == 0),
        Results(),
        # CopyTransformer('eval.acc', 'ea'),
        # CollectRows(),
        # FilterList(lambda r: r['selected']),
        # Charter(),
        # Counter()
    ]

    try:
        logger.remove(0)
    except Exception:
        pass
    logger.add(sys.stderr, level="INFO", colorize=True, enqueue=True,
               format="<green>{time:HH:mm:ss}[{process.id}] | </green><level> {level}: {message}</level>")

    pipeline = Pipeline(pipe)
    out_path = await pipeline.run(input_path)


if __name__ == '__main__':
    asyncio.run(main())

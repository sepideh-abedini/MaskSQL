from os import pathconf

from pyasn1_modules.rfc5280 import policyQualifierInfoMap

from src.pipe.processor.list_transformer import JsonListTransformer
from src.pipe.sqlite_facade import SqliteFacade
from src.util.json_utils import read_json, write_json


class CalcExecAcc(JsonListTransformer):
    def __init__(self, database_dir, policy):
        super().__init__(False)
        self.dbf = SqliteFacade(database_dir)
        self.count = 0
        self.policy = policy
        self.failures_arr= []

    async def _process_row(self, row):
        gold = row['query']
        pred = row['pred_sql']
        db_id = row['db_id']
        self.count += 1
        try:
            gold_res, _ = self.dbf.exec_query_sync(db_id, gold)
            pred_res, err = self.dbf.exec_query_sync(db_id, pred)
            if gold_res == pred_res:
                acc = 1
            else:
                acc = 0
                self.failures_arr.append(row['question_id'])

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

    def _post_run(self):
        self.failures(self.failures_arr)

    def failures(self, arr):
        path= f"data/{self.policy}/EA_failures.json"
        write_json(path,arr)




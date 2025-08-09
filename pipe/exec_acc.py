import os
import sqlite3

from pipe.processor.list_processor import JsonListProcessor
from pipe.processor.list_transformer import JsonListTransformer
from pipe.sqlite_facade import SqliteFacade


class ExecAccCalc(JsonListTransformer):
    def __init__(self, database_dir):
        super().__init__(False)
        self.dbf = SqliteFacade(database_dir)

    async def _process_row(self, row):
        gold = row['query']
        pred = row['pred_sql']
        db_id = row['db_id']
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
            return row
        except Exception as e:
            print(e)
            raise e

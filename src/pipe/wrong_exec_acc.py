from loguru import logger

from src.pipe.processor.list_transformer import JsonListTransformer
from src.pipe.sqlite_facade import SqliteFacade


class ExecuteConcreteSql(JsonListTransformer):
    async def _process_row(self, row):
        result = await self.get_exec_acc(row)
        return result

    def __init__(self, database_dir):
        super().__init__(False)
        self.dbf = SqliteFacade(database_dir)

    async def get_exec_acc(self, row):
        gold = row['query']
        pred = row['concrete_sql']
        db_id = row['db_id']
        try:
            gold_res, _ = self.dbf.exec_query_sync(db_id, gold)
            pred_res, pred_err = self.dbf.exec_query_sync(db_id, pred)
            if gold_res == pred_res:
                acc = 1
            else:
                acc = 0
            if pred_res is not None and len(pred_res) > 5:
                logger.debug(f"Pred results was limited: original size = {len(pred_res)}")
                pred_res = pred_res[:5]
            if pred_err is None:
                pred_err = ""
            # if pred_err is not None:
            #     err = pred_err
            # elif acc == 0:
            #     err = "The predicted SQL is executable but the execution result is different from the gold execution result"
            # else:
            #     err = None
            row["pre_eval"] = {
                "acc": acc,
                "err": pred_err,
                "pred_res": pred_res
            }
            return row
        except Exception as e:
            print(e)
            raise e

    # async def run(self, input_file):
    #     output_file = self.get_output_file(input_file)
    #     if not self.force and os.path.exists(output_file):
    #         print(f"File exists: {output_file}, skipping.")
    #         return output_file
    #
    #     with open(input_file) as f:
    #         in_data = json.load(f)
    #
    #     output_rows = []
    #     for i, row in enumerate(tqdm.tqdm(in_data, desc=self.name, total=len(in_data))):
    #         exec_acc = await self.get_exec_acc(row)
    #         row['exec_acc'] = exec_acc
    #         if exec_acc == 0:
    #             output_rows.append(row)
    #
    #     with open(output_file, "w") as f:
    #         f.write(json.dumps(output_rows, indent=4))
    #     return output_file

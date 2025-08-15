import asyncio
import os
import sys

from loguru import logger

from ut.json_utils import read_json
from pipe.pipeline import Pipeline
from pipe.processor.limit_list import LimitJson
from pipe.processor.list_transformer import JsonListTransformer
from pipe.schema_repo import DatabaseSchemaRepo

LLM_MODEL = os.getenv("LLM_MODEL")
SLM_MODEL = os.getenv("SLM_MODEL")
VLM_MODEL = os.getenv("VLM_MODEL")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

out_dir = os.path.join("out", "new_fine")

if not os.path.exists(out_dir):
    os.makedirs(out_dir, exist_ok=True)

database_path = "../parser/data/bird/database"
input_path = os.path.join(out_dir, "1_input.json")
tables_path = os.path.join(out_dir, "tables.json")


class AddDbId(JsonListTransformer):

    def __init__(self):
        super().__init__(force=True)
        self.data = read_json("out/fine/bird_train_sel/1_input.json")

    async def _process_row(self, row):
        idx = row['idx']
        orig = self.data[idx]
        row['db_id'] = orig['db_id']
        return row


class CheckLinks(JsonListTransformer):

    def __init__(self, tables_path):
        super().__init__(force=True)
        self.schema_repo = DatabaseSchemaRepo(tables_path)
        self.count = 0

    def _post_run(self):
        print(self.count)

    async def _process_row(self, row):
        schema = self.schema_repo.dbs[row['db_id']]
        row['schema'] = schema.to_yaml()
        links = row['final_links']
        question = row['question']
        idx = row['idx']
        for q_term in links.keys():
            if q_term.lower() not in question.lower():
                raise RuntimeError(f"#{idx}-{q_term} not in {question}")

        for schema_item in links.values():
            if not isinstance(schema_item, list):
                schema_item = [schema_item]
            for si in schema_item:
                [item_type, ref] = si.split(":")
                if item_type == "TABLE":
                    if ref not in schema.tables:
                        self.count += 1
                        print(f"${idx}", ref)
                else:
                    found = False
                    [_, col] = ref.split(".")
                    if "*" in col:
                        found = True
                    for t, cols in schema.tables.items():
                        if col in cols:
                            found = True
                    if not found:
                        print(f"#{idx} {ref}")
                        print(schema.to_yaml())
                        self.count += 1
        return row


mask_pipe = [
    # LimitJson("limit"),
    AddDbId(),
    CheckLinks(tables_path)
]


async def main():
    try:
        logger.remove(0)
    except Exception:
        pass
    logger.add(sys.stderr, level=LOG_LEVEL, colorize=True, enqueue=True,
               format="<green>{time:HH:mm:ss}[{process.id}] | </green><level> {level}: {message}</level>")

    pipeline = Pipeline(mask_pipe)
    out_path = await pipeline.run(input_path)
    print("LLM MODEL:", LLM_MODEL)
    print("SLM MODEL:", SLM_MODEL)


if __name__ == '__main__':
    asyncio.run(main())

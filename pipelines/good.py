import asyncio
import os
import sys
from typing import Dict

from loguru import logger

from pipe.pipeline import Pipeline
from pipe.processor.limit_list import FilterList
from pipe.processor.list_transformer import JsonListTransformer
from pipelines.eval import Results

out_dir = os.path.join("out", "dataset_msc_0_400_good")

if not os.path.exists(out_dir):
    os.makedirs(out_dir, exist_ok=True)

database_path = "../parser/data/bird/database"
input_path = os.path.join(out_dir, "1_input.json")
tables_path = os.path.join(out_dir, "tables.json")


class FixFormat(JsonListTransformer):
    def __init__(self):
        super().__init__()

    async def _process_row(self, row: Dict) -> Dict:
        row['query'] = row['SQL']
        row['msc_ea'] = row['eval']['acc']
        del row['eval']
        del row['gold']
        del row['pred']
        return row


class Analyze(JsonListTransformer):
    def __init__(self):
        super().__init__()
        self.msc = 0
        self.gpt = 0
        self.count = 0
        self.gpt_better = 0
        self.both_bad = 0
        self.both_good = 0
        self.msc_better = 0

    def _post_run(self):
        print("MSC:", self.msc)
        print("GPT:", self.gpt)
        print("G>=:", self.gpt_better)
        print("M>=:", self.msc_better)
        print("BADD", self.both_bad)
        print("Good", self.both_good)
        print("TOT:", self.count)

    async def _process_row(self, row: Dict) -> Dict:
        gpt_ea = row['eval']['acc']
        msc_ea = row['msc_ea']
        if gpt_ea == 1 and msc_ea == 0:
            self.gpt_better += 1
        if gpt_ea == 0 and msc_ea == 0:
            self.both_bad += 1
        if gpt_ea == 1 and msc_ea == 1:
            self.both_good += 1
        if gpt_ea == 0 and msc_ea == 1:
            self.msc_better += 1
        self.gpt += gpt_ea
        self.msc += msc_ea

        self.count += 1


pipe = [
    # FilterList(lambda r: r['eval']['acc'] == 1),
    Analyze()
    # Results(),
]


async def main():
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

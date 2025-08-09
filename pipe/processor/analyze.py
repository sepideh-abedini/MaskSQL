from pipe.processor.list_processor import JsonListProcessor
from src.cat.catter import Catter


class AnalyzeResults(JsonListProcessor):
    def __init__(self):
        super().__init__()
        self.catter = Catter()

    def _post_run(self):
        print("done")

    async def _process_row(self, row):
        sql = row['query']
        cat = self.catter.get_category(sql)
        sub = self.catter.get_sub_category(sql)
        print(f"{cat}:{sub}")
        # print(f"GOLD: {sql}")

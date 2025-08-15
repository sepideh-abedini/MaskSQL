import asyncio
import os
from typing import Dict

from pipe.pipeline import Pipeline
from pipe.processor.limit_list import FilterList
from pipe.processor.list_transformer import JsonListTransformer
from pipe.processor.printer import LambdaPrinter
from src.cat.catter import Catter
from ut.json_utils import write_json

catter = Catter()

out_dir = os.path.join("out", "fine", "bird_train")
input_path = os.path.join(out_dir, "1_input.json")
tables_path = os.path.join(out_dir, "tables.json")


class AssignCategory(JsonListTransformer):
    def __init__(self):
        super().__init__(force=False)

    async def _process_row(self, row: Dict) -> Dict:
        sql = row['SQL']
        cat = catter.get_category(sql)
        row['cat'] = cat.name
        return row


class Counter(JsonListTransformer):
    def __init__(self):
        super().__init__()
        self.count = 0

    def _post_run(self):
        print(f"Count = {self.count}")

    async def _process_row(self, row: Dict) -> Dict:
        self.count += 1
        return row


class DataCollector(JsonListTransformer):
    def __init__(self):
        super().__init__()
        self.dbs = dict()

    def _post_run(self):
        selected_rows = []
        for db_id in self.dbs:
            selected_rows.extend(self.dbs[db_id][:50])

        write_json(os.path.join(out_dir, 'bird_train_sel.json'), selected_rows)

    async def _process_row(self, row: Dict) -> Dict:
        db_id = row['db_id']
        self.dbs.setdefault(db_id, []).append(row)
        return row


excluded = [
    'movie_3',
    'bike_share_1',
    'human_resources',
    'craftbeer',
    'food_inspection',
    'chicago_crime',
    'software_company',
    'sales_in_weather',
    'university',
    'music_platform_2',
    'world',
    'hockey',
    'image_and_language',
    'works_cycles',
    'ice_hockey_draft',
    'retails',
    'retail_world',
    'coinmarketcap',
    'food_inspection_2',
    'airline',
    'language_corpus',
    'menu',
    'sales',
    'beer_factory',
    'address',
    'legislator',
    'disney',
    'mental_health_survey',
    'student_loan',
    'simpson_episodes',
    'citeseer',
    'public_review_platform',
    'college_completion',
    'authors',
    'donor',
    'shakespeare',
    'professional_basketball',
    'european_football_1',
    'regional_sales',
    'app_store',
    'genes',
    'movielens',
    'world_development_indicators',
    'music_tracker',

]
selected = [
    'cookbook',
    'mondial_geo',
    'books',
    'shipping',
    'olympics',
    'video_games',
    'cars',
    'shooting',
    'superstore',
    'soccer_2016'
]

pl = [
    AssignCategory(),
    FilterList(lambda r: r['cat'] in ['c4', 'c5', 'c6']),
    # FilterList(lambda r: r['db_id'] not in excluded),
    FilterList(lambda r: r['db_id'] in selected),
    DataCollector()
    # LambdaPrinter(lambda r: print(
    #     f"DB ID: {r['db_id']}\nQuestion: {r['question']}\nCat:{r['cat']}\nSQL: {r['SQL']}\n{'-' * 50}")),
    # Counter()
]


async def main():
    pipeline = Pipeline(pl)
    await pipeline.run(input_path)


if __name__ == '__main__':
    asyncio.run(main())

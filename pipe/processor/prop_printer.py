from typing import List

from pipe.processor.list_processor import JsonListProcessor


class PrintProps(JsonListProcessor):
    def __init__(self, props: List[str]):
        super().__init__()
        self.props = props


    async def _process_row(self, row):
        # if row['pre_eval']['acc'] == 0 and row['eval']['acc'] == 1:
        if row['eval']['acc'] == 0:
            print("Entry: " + "-" * 20)
            for prop in self.props:
                print(f"{prop}:\n {self.get_prop(row, prop)}")
        return row

import json
import os

from pipe.processor.list_transformer import JsonListTransformer


class CopyTransformer(JsonListTransformer):

    def __init__(self, src, dst):
        super().__init__(force=True)
        self.src = src
        self.dst = dst

    async def _process_row(self, row):
        src_value = self.get_prop(row, self.src)
        self.set_prop(row, self.dst, src_value)
        return row

class DeleteProp(JsonListTransformer):
    def __init__(self, prop):
        super().__init__(force=True)
        self.prop = prop

    async def _process_row(self, row):
        del row[self.prop]
        return row




class CopyFromPrevStage(JsonListTransformer):

    def __init__(self, stage, src):
        super().__init__(force=True)
        self.stage = stage
        self.src = src

    def get_prev_stage(self, input_file):
        dir_path = os.path.dirname(input_file)
        prev_stage_file_path = os.path.join(dir_path, f"{self.stage}.json")
        return super()._get_input_data(prev_stage_file_path)

    async def run(self, input_file):
        output_file = await super().run(input_file)

        with open(output_file) as f:
            data = json.load(f)

        prev_stage = self.get_prev_stage(input_file)

        updated_rows = []
        for i, row in enumerate(data):
            row[self.src] = prev_stage[i][self.src]
            updated_rows.append(row)

        with open(output_file, "w") as f:
            f.write(json.dumps(updated_rows, indent=4))
        return output_file

    async def _process_row(self, row):
        return row


class AddGoldValues(JsonListTransformer):

    def __init__(self):
        super().__init__(force=True)

    async def _process_row(self, row):
        value_links = row['gold_value_links']
        keys = list(value_links.keys())
        row['values'] = keys
        return row

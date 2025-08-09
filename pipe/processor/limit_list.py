import json
import os

from pipe.processor.list_transformer import JsonListTransformer

START = int(os.environ.get("START", 0))
LIMIT = int(os.environ.get("LIMIT", 10))


class LimitJson(JsonListTransformer):

    async def run(self, input_file):
        output_file = self.get_output_file(input_file)

        with open(input_file) as f:
            in_data = json.load(f)

        out_data = in_data[START:START + LIMIT]

        out_rows = []
        for row in out_data:
            row['total_toks'] = 0
            out_rows.append(row)

        with open(output_file, "w") as f:
            f.write(json.dumps(out_rows, indent=4))
        return output_file

    async def _process_row(self, row):
        return row

from pipe.processor.list_transformer import JsonListTransformer


class CopyTransformer(JsonListTransformer):

    def __init__(self, src, dst):
        super().__init__(force=True)
        self.src = src
        self.dst = dst

    async def _process_row(self, row):
        src_value = self.get_prop(row, self.src)
        row[self.dst] = src_value
        return row


class AddGoldValues(JsonListTransformer):

    def __init__(self):
        super().__init__(force=True)

    async def _process_row(self, row):
        value_links = row['gold_value_links']
        keys = list(value_links.keys())
        row['values'] = keys
        return row

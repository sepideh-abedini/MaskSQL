from pipe.processor.list_transformer import JsonListTransformer


class AddValueLinksFromSchemaLinks(JsonListTransformer):

    async def _process_row(self, row):
        schema_links = row['schema_links']
        value_links = dict()
        updated_schema_links = dict()
        for q_term, item in schema_links.items():
            if "VALUE:" in item:
                item = item.replace("VALUE:", "")
                value_links[q_term] = item
            else:
                updated_schema_links[q_term] = item
        row['schema_links'] = updated_schema_links
        row['value_links'] = value_links
        return row

SCHEMA_LINK_PROMPT_V2 = """
Consider the following question:
Question: 
{question}

To write a SQL query for this question schema items from the following list are used:
{schema_items}

Each schema item is either a table name or a fully qualified column name.

Complete the following dict:
{schema_links_dict}

In this dict, keys are 2-grams of the question. You should fill values with the most relevant schema item.
For some 2-grams, there might be no relevant schema item. In this case, fill the value with None.
Do not output any comments. Output a valid json object.
"""

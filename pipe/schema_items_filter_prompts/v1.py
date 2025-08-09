FILTER_SCHEMA_ITEMS_PROMPT_V1 = """
You are an assistant that filters a list of a database schema items based on their relevance to a set of concepts.

Input:
    Schema Items: a list of table names and fully qualified column names. Each Schema Item is of the form 
    "TABLE:[table_name]" or "COLUMN:[table_name].[column_name]". 

Goal:
Return a filtered list of schema items that contains only those that are related to at least one the following concepts:
{concepts}

Output Rules
- Do not add, alter, or rename any item.
- Output should be a valid JSON list.
- Do not include any additional text, explanations, or formatting.

Example:
Schema Items:
[
    "COLUMN:[instructor].[name]",
    "COLUMN:[instructor].[salary]",
    "TABLE:[instructor]"
]

Output:
[
    "name": "COLUMN:[instructor].[name]",
]

Now filter the following Schema Items:
Schema Items: {schema_items}
"""

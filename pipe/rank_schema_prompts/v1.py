RANK_SCHEMA_ITEMS_V1 = """
You are given:
	1. A natural language question.
	2. A list of schema items of an underlying database. Each schema item is either 
	"TABLE:[table_name]" or "COLUMN:[table_name].[column_name]

Task:
Filter the given list and return a subset of these items that are most relevant to the given question.
You can include at most 4 tables and at most 5 columns for each table.

Example:
Question: “What is the name of the instructor who has the lowest salary?”
Schema Items:
[
    "TABLE:[department]",
    "COLUMN:[department].[name]",
    "TABLE:[instructor]",
    "COLUMN:[instructor].[name]"
    "COLUMN:[instructor].[salary]"
    "COLUMN:[instructor].[age]"
]

Output:
[
    "TABLE:[instructor]",
    "COLUMN:[instructor].[name]"
    "COLUMN:[instructor].[salary]"
]

Now filter the following list of Schema Items based on the given question.
Question: {question}
Schema Items: {schema_items}

Instructions:
- Output only a valid list of strings.
- Do not include any additional text, explanations, or formatting.:
- All strings should be in double quotes.
"""

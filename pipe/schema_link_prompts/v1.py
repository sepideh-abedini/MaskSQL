SCHEMA_LINK_PROMPT_V1 = """
Consider the following question:
Question: 
{question}

To write a SQL query for this question schema items from the following list are used:
{schema_items}

Each schema item is either a table name or a fully qualified column name.

Example:
Question: "What is the name of the instructor who has the lowest salary?"
Schema items: 
[ "[instructor].[name]", "[instructor].[salary]", "[department].[name]"]

Output: 
```json
{{
    "name": "[instructor].[name]",
    "salary": "[instructor].[salary]"
}}
```

Give me a dict from words in the most relevant schema items. 
Exclude words that don't match with any schema item.
Question: {question}
Only output the result, no explanation.
Result should be in the form of dictionary from words of the question to a single schema item.
Note that all schema items might not be used in the question.
"""

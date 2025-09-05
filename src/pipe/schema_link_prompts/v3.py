SCHEMA_LINK_PROMPT_V3 = """
You are given a natural language question and a list of schema items 
(table names or fully qualified column names).

Task:
Identify a mapping from n-grams (sub-sequences of up to 3 consecutive words) 
in the question to the most relevant schema item. 
Each mapping is a key-value pair where the key is a n-gram and the value is a schema item.
Schema items are either table names or fully qualified column names.

Example:
Question: “What is the name of the instructor who has the lowest salary?”
Schema items:
["[instructor].[name]", "[instructor].[salary]", "[department].[name]"]

Output:
{{
    "name": "COLUMN:[instructor].[name]",
    "salary": "COLUMN:[instructor].[salary]",
    "instructor": "TABLE:[instructor]"
}}

Now complete the task:
Question: {question}
Schema items: {schema_items}

Instructions:
- Output only a JSON object representing the mapping.
- Do not include any additional text, explanations, or formatting.
- All json key and values should be in double quotes.
"""


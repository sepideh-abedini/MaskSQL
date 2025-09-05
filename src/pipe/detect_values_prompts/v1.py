PROMPT = """
You are given:
	1.	A natural language question.
	2.	A mapping (SchemaLinks) from n-grams in the question to relevant table or column names 
	in a database schema.

Task:
Identify which n-gram in the question, is related to the value of a column for some row
in the table. Return an updated mapping where the prefix of those schema items is changed
from COLUMN: to VALUE:.

Example:
Question: “What is the name of the instructor who located in London?”
SchemaLinks:
{{
    "name": "COLUMN:[instructor].[name]",
    "instructor": "TABLE:[instructor]",
    "London": "COLUMN:[instructor].[location]"
}}

Output:
{{
    "name": "COLUMN:[instructor].[name]",
    "instructor": "TABLE:[instructor]",
    "London": "VALUE:[instructor].[location]"
}}

Now perform the task:
Question: {question}
SchemaLinks: {schema_links}

Instructions:
- Output only a JSON object representing the filtered mapping.
- Do not include any additional text, explanations, or formatting.
- All json key and values should be in double quotes.
"""

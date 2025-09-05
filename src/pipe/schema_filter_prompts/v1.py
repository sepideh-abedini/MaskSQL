FILTER_SCHEMA_LINKS_PROMPT_V1 = """
You are given:
	1.	A natural language question.
	2.	A mapping (SchemaLinks) from n-grams in the question to relevant table or column names 
	in a database schema.

Task:
Filter the SchemaLinks mapping so that it only includes entries related to the following concepts:
{concepts}

Example:
Question: “What is the name of the instructor who has the lowest salary?”
SchemaLinks:
{{
    "name": "COLUMN:[instructor].[name]",
    "salary": "COLUMN:[instructor].[salary]",
    "instructor": "TABLE:[instructor]"
}}

Output:
{{
    "name": "COLUMN:[instructor].[name]",
}}

Now perform the task:
Question: {question}
SchemaLinks: {schema_links}

Instructions:
- Output only a JSON object representing the filtered mapping.
- Do not include any additional text, explanations, or formatting.:
- All json key and values should be in double quotes.
"""

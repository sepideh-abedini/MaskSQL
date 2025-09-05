FILTER_ANNOTATED_LINKS = """
You are an assistant that filters a given dictionary to retain items that are related to a set of concepts.

You are given:
	1.	A natural language question.
	2.	A mapping (SchemaLinks) from n-grams in the question to relevant table or column names 
	in a database schema.

Goal:
Return a filtered JSON object that contains only those key-value pairs from SchemaLinks that are 
related to at least one the following concepts:
{concepts}

Output Rules
- Do not add, alter, or rename keys or values. Only delete non-matching entries.
- Output valid JSON only: double quotes around all keys and string values; no trailing commas.
- If no entries match, return an empty JSON object.
- Do not include any additional text, explanations, or formatting.

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

Now filter the following SchemaLinks mapping based on the given question and concepts.
You should generate a valid JSON object.
Question: {question}
SchemaLinks: {schema_links}

"""

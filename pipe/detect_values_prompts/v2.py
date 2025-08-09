DETECT_VALUES_PROMPT_V2 = """
You are given:
	1. A natural language question.
	2. A mapping (SchemaLinks) from n-grams in the question to relevant table or column names 
	in a database schema. Each schema item is either "TABLE:[table]" or "COLUMN:[table].[column]".
	3. A list of n-grams in the question that represent literal values, entities, constants, etc in the question.

Goal
Produce an updated JSON object with the same keys, in the same order, 
changing the prefix of the dictionary values (schema items) from "COLUMN:" to "VALUE:" 
only for those entries whose key text (n-gram of the question) in the question represents 
a literal value appearing in that column (as the value of that column for some row of the database). 
Leave all other entries exactly as they are.

When to change COLUMN: -> VALUE:
Change to VALUE: if, in the question, the n-gram key:
- Is a literal string/number/date token (e.g., “London”, “50000”, “2021”) that stands for some row’s value in the mapped column.
- Appears in a filtering context that assigns or compares a value to that column
 (patterns like in, at, from, where, with, =, >, <, between, after, before, etc.).
- Is a proper noun or quoted phrase that would naturally live in that column 
(city in a location column, person name in a name column) and is not itself the column label.
- Always keep TABLE: entries unchanged.

Output Rules:
- Output valid JSON only: double-quoted keys and values; no trailing commas.
- Do not add, drop, or reorder keys.
- Change only the COLUMN: prefix to VALUE: where warranted; keep everything else unchanged.
- If no changes, return the input JSON unchanged.

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

Now identify the values and update the following SchemaLinks mapping based on the following question. 
Question: {question}
SchemaLinks: {schema_links}
"""

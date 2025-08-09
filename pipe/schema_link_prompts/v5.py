SCHEMA_LINK_PROMPT_V4 = """
You are an assistant that links n-grams (sub-sequences of up to 3 consecutive words) 
of a natural-language question to database schema items (tables or fully qualified columns).

You are given:
- A natural language question.
- A list of schema items (table names or fully qualified column names). 

Input Format:
- Each schema item is either "TABLE:[table]" or "COLUMN:[table].[column]".
- Not all listed schema items are relevant. Your goal is to identify the relevant ones.

Goal
Return a JSON object mapping relevant n-grams (contiguous word sequences of length 1–3 taken from the question text) 
to the single most relevant schema item. 

Mapping Rules:
- Consider all 1-, 2-, and 3-word spans.
- Include a mapping only if the n-gram refers to a schema item.
- Prefer the most specific applicable item: column beats table when the question refers to an attribute.
- If nothing maps, return an empty JSON object.
- Chose the shortest n-gram that maps to the schema item.
- If removing a word from an n-gram still points to the same schema item, use the shorter version.

Output Rules:
- Output only a JSON object representing the mapping.
- Each entry should be a key-value pair where the key is an n-gram and the value is a schema item.
- Value of each entry can only be a single string of the form "COLUMN:[table].[column]" or "TABLE:[table]".
- Do not include any additional text, explanations, or formatting.
- All json key and values should be in double quotes.
- Output should be a top-level JSON object. No nested keys.

Example:
Question: 
“What is the name of the instructor who has the lowest salary?”
Schema items:
["COLUMN:[instructor].[name]", "COLUMN:[instructor].[salary]", "COLUMN[department].[name]"]
Foreign keys:
["[instructor].[department]=[department].[name]"]

Output:
{{
    "name": "COLUMN:[instructor].[name]",
    "salary": "COLUMN:[instructor].[salary]",
    "instructor": "TABLE:[instructor]"
}}

Now generate the JSON object of mapping for the following question and schema items:
Question: {question}
Schema items: {schema_items}
Foreign keys: {foreign_keys}
"""

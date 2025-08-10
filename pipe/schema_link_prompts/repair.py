REPAIR_SCHEMA_LINK_PROMPT_V1 = """
You are an assistant that links n-grams (sub-sequences of up to 3 consecutive words) 
of a natural-language question to database schema items (tables or fully qualified columns).
Your goal is to repair a given schema links. 
Keys of the dictionary are n-grams in the question and values or schema items.
Your goal is to make sure that the given schema links is correct according to the following rules.

You are given:
- Question: a natural language question.
- Schema Items: a list of schema items (table names or fully qualified column names). 
- Value List: a list of n-grams in the question that represent literal values, entities, constants, etc in the question.
- Schema Links: a dictionary that maps schema n-grams of the question to the schema items

Goal:
Iterate through each key,value of the mapping and verify:
- Each key s a n-gram of the question
- Each value is a schema item included in the provided schema items list
- Each key doesn't exist in the given value list
- Do not change the key-value if its is correct

If you found any errors, fix the issues with the minimum change by replacing some words.
Return the repaired schema link mapping.

Here are some examples:

---------------------------------------------
Example 1:
Question: 
“What is the name of the instructor who has the lowest salary and located in London?”
Schema items:
["TABLE:[instructor]", "COLUMN:[instructor].[name]", "COLUMN:[instructor].[salary]", "TABLE:[department]", "COLUMN[department].[name]"]
Value List: 
[ "London" ]
Schema Links:
{{
    "lowest salary": "COLUMN:[instructor].[salary]",
    "who": "TABLE:[instructor]"
}}

Output:
{{
    "name": "COLUMN:[instructor].[name]",
    "salary": "COLUMN:[instructor].[salary]",
    "instructor": "TABLE:[instructor]"
}}

Now generate the repaired JSON object of mapping for the following question, schema items, value list, and schema links:
Question: {question}
Schema items: {schema_items}
Value List: {value_List}
Schema Links: {schema_links}
"""

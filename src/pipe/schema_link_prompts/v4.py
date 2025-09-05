SCHEMA_LINK_PROMPT_V4 = """
You are an assistant that links n-grams (sub-sequences of up to 3 consecutive words) 
of a natural-language question to database schema items (tables or fully qualified columns).

You are given:
- Question: a natural language question.
- Schema Items: a list of schema items (table names or fully qualified column names). 
- Value List: a list of n-grams in the question that represent literal values, entities, constants, etc in the question.

Input Format:
- Each schema item is either "TABLE:[table]" or "COLUMN:[table].[column]".
- Not all listed schema items are relevant. Your goal is to identify the relevant ones.

Goal
Return a JSON object mapping relevant n-grams (contiguous word sequences of length 1–3 taken from the question text) 
to the single most relevant schema item. 

Mapping Rules:
- You should not provide mapping for the n-grams included in the Value List
- Consider all 1-, 2-, and 3-word spans.
- Include a mapping only if the n-gram refers to a schema item.
- Prefer the most specific applicable item: column beats table when the question refers to an attribute.
- If nothing maps, return an empty JSON object.
- Chose the shortest n-gram that maps to the schema item.
- If removing a word from an n-gram still points to the same schema item, use the shorter version.

Output Rules:
- Output only a JSON object representing the mapping.
- The value of each entry should only be selected from the given list of Schema Items. 
- Generating new values or using different values is not allowed.
- You can only select values form the given list of schema items.
- Each entry should be a key-value pair where the key is an n-gram and the value is a schema item.
- Value of each entry can only be a single string of the form "COLUMN:[table].[column]" or "TABLE:[table]".
- Do not include any additional text, explanations, or formatting.
- All json key and values should be in double quotes.
- Output should be a top-level JSON object. No nested keys.

Here are some examples:

---------------------------------------------
Example 1:
Question: 
“What is the name of the instructor who has the lowest salary and located in London?”
Schema items:
["TABLE:[instructor]", "COLUMN:[instructor].[name]", "COLUMN:[instructor].[salary]", "TABLE:[department]", "COLUMN[department].[name]"]
Value List: 
[ "London" ]

Output:
{{
    "name": "COLUMN:[instructor].[name]",
    "salary": "COLUMN:[instructor].[salary]",
    "instructor": "TABLE:[instructor]"
}}

---------------------------------------------
Example 2:
Question: 
"Please calculate the total payment amount of customers who come from the USA. USA is a country; total amount payment refers to SUM(amount);",
Schema items: [
    "TABLE:[customers]",
    "COLUMN:[customers].[customernumber]",
    "COLUMN:[customers].[country]",
    "TABLE:[payments]",
    "COLUMN:[payments].[customernumber]",
    "COLUMN:[payments].[amount]"
]
Value List: 
[ "USA" ]

Output:
{{
    "customers": "TABLE:[customers]",
    "country": "COLUMN:[customers].[country]",
    "amount": "COLUMN:[payments].[amount]"
}}

---------------------------------------------
Example 3:
Question:
"What are the total payments of customers with no credit limit in 2003? total payment refers to SUM(amount)",
Schema Items: [
    "TABLE:[customers]",
    "COLUMN:[customers].[customernumber]",
    "COLUMN:[customers].[creditlimit]",
    "TABLE:[payments]",
    "COLUMN:[payments].[customernumber]",
    "COLUMN:[payments].[paymentdate]",
    "COLUMN:[payments].[amount]"
]
Value List:
[ "2003" ]

Output:
{{
    "payments": "TABLE:[payments]",
    "customers": "TABLE:[customers]",
    "credit limit": "COLUMN:[customers].[creditlimit]",
    "amount": "COLUMN:[payments].[amount]"
}}



Now generate the JSON object of mapping for the following question, schema items, and value list:
Question: {question}
Schema items: {schema_items}
Value List: {value_List}

Iterate through each key,value pair of the answer and make sure that:
- MAKE SURE THAT EACH KEY OF THE MAPPING SHOULD BE A TERM OF THE QUESTION
- MAKE SURE THAT EACH VALUE OF THE MAPPING SHOULD BE A VALID SCHEMA ITEM INCLUDED IN THE GIVEN LIST OF SCHEMA ITEMS 
- MAKE SURE THAT EACH KEY BE MINIMAL, IF ANY WORD CAN BE DELETED WHILE THE RELATION STILL HOLDS, IT SHOULD BE REMOVED
"""

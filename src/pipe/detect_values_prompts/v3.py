DETECT_VALUES_PROMPT_V3 = """
You are given a natural language question and a list of schema items
(table names or fully qualified column names).
The question is a textual representation of some SQL query a database for which we have the schema items.
Your goal is to find a list of literal values, entities, constants, etc in the question.
Database schema is given to exclude table or column names as these values.

Output Format:
- Output should be a list of strings
- Each string should be quoted with double quotes. 

Here are some Examples:

---------------------------------
Example 1:
Question: "What is the name of the instructor who located in London?"
Output:
["London"]

---------------------------------
Example 2:
Question: "State the email of those who are staff of Murphy Diane whose number is 1002 and living in San Francisco staff of refers to reportsTO"
Output:
["Murphy Diane", "1002", "San Francisco"]

---------------------------------
Example 3:
Question: Determine the email and Code of employee who are working at United State, state MA;
Output:
["United State", "MA"]

---------------------------------
Example 4:
Question: “Show me all reservations under the name David Johnson for hotel Hilton on 12/25/2023 with booking code 8793.”
Output:
["David Johnson", "Hilton", "12/25/2023", "8793"]

Now generate the output list for the following question: 
Question: {question}
Schema: {schema_items}
"""

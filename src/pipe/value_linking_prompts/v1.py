VALUE_LINKING_PROMPT_V1 = """
You are given:
	Question: A natural language question.
	Values List: A list of n-grams in the question that represent literal values, entities, constants, etc in the question.
    Column Names: A list of fully qualified column names of an underlying database. 
    
Goal
Return a JSON object mapping from the Value List to the single most relevant column item. 

Mapping Rules:
- Consider all 1-, 2-, and 3-word spans.
- Chose the shortest n-gram that relates to a column.
- If removing a word from an n-gram still points to the same column, use the shorter version.
- You should link a value only to columns, not tables.
- The values of the map should be selected only from the given list of column names, no value should
be added or changed.

Output Rules:
- Output valid JSON only: double-quoted keys and values; no trailing commas.
- Do not add, drop, or reorder keys.
- Change only the COLUMN: prefix to VALUE: where warranted; keep everything else unchanged.
- If no changes, return the input JSON unchanged.

Here are some Examples:

---------------------------------------------
Example 1:
Question: “What is the name of the instructor who located in London?”
Values List: 
[ "London" ]
Column Names:
[
    "[instructor].[name]",
    "[instructor].[location]"
]

Output:
{{
    "London": "[instructor].[location]"
}}

---------------------------------------------
Example 2:
Question: 
"How many different orders with a total price greater than 4000 are cancelled? total price = MULTIPLY(quantityOrdered, priceEach) > 4000; cancelled orders refer to status = 'Cancelled';",
Value List:
["Euro+ Shopping Channel", "2004"]
Column Names: [ 
    "[customers].[customernumber]",
    "[customers].[customername]",
    "[payments].[customernumber]",
    "[payments].[checknumber]",
    "[payments].[paymentdate]"
]

Output:
{{
    "Euro+ Shopping Channel": "[customers].[customername]",
    "2004": "[payments].[paymentdate]"
}}

---------------------------------------------
Example 3:
Question: 
"State the email of those who are staff of Murphy Diane whose number is 1002 and living in San Francisco staff of refers to reportsTO; San Francisco is a city;",
Value List:
[ "Murphy Diane", "1002", "San Francisco" ]
Column Names: [ 
    "[employees].[employeenumber]",
    "[employees].[firstname]",
    "[employees].[lastname]",
    "[employees].[email]",
    "[employees].[reportsto]",
    "[employees].[officecode]",
    "[offices].[officecode]",
    "[offices].[city]"
]
Output:
{{
    "Murphy Diane": "[employees].[reportsto]",
    "1002": "[employees].[employeenumber]",
    "San Francisco": "[offices].[city]"
}}

Now generate the mapping for the following Values List and Column Names based on the given question. 
Question: {question}
Values List: {values}
Column Names: {columns}
"""

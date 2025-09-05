VALUE_LINKS_FILTER_PROMPT_V1 = """
You are given:
	Question: a natural language question.
	Value Links: a mapping from n-grams in the question to their relevant columns of a database schema.

Task:
Filter the mapping object so that it only includes entries related to the following concepts:
{concepts}

Here are some examples:

---------------------------------------------
Example 1:
Question: “What is the name of the instructor who located in London and having a Ferrari?”
Value Links:
{{
    "London": "[instructor].[location]",
    "Ferrari": "[instructor].[car]",
}}

Output:
{{
    "London": "[instructor].[location]",
}}

---------------------------------------------
Example 2:
Question: 
"State the email of those who are staff of Murphy Diane whose number is 1002 and living in San Francisco staff of refers to reportsTO; San Francisco is a city;",
Value Links:
{{
    "Murphy Diane": "[employees].[reportsto]",
    "1002": "[employees].[employeenumber]",
    "San Francisco": "[offices].[city]"
}}

Output:
{{
    "Murphy Diane": "[employees].[reportsto]",
    "San Francisco": "[offices].[city]"
}}

---------------------------------------------
Example 3:
Question: 
"How many customers who are in Norway and have credit line under 220000? Norway is a country;",
Value Links:
{{
    "Norway": "[customers].[country]",
    "220000": "[customers].[creditlimit]"
}}

Output:
{{
    "Norway": "[customers].[country]"
}}


Now perform the task:
Question: {question}
Value Links: {value_links}

Instructions:
- Output only a JSON object representing the filtered mapping.
- Do not include any additional text, explanations, or formatting.:
- All json key and values should be in double quotes.
"""

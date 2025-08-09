REPAIR_SYMBOLIC_SQL_PROMPT_V1 = """
You are an SQL database expert tasked with correcting a SQL query. 
A previous attempt to run a query did not yield the correct results, 
either due to errors in execution or because the result returned was empty or unexpected. 
Your role is to analyze the error based on the provided database schema and the details 
of the failed execution, and then provide a corrected version of the SQL query.

**Procedure:** 
1. Review Database Schema: 
    - Examine the database schema to understand the database structure.
    - Iterate through the each column and table name in the schema to make sure that it is correct.
    - Some table or column names may have white space, you should not change these and use a different name.
    - Database schema is given in YAML format where top-level keys are table names; each table lists its columns and their data types.
    - Column names are case-sensitive exactly as shown in the schema.
    - Each column might be primary key or a foreign key.
    - For foreign key columns, fully qualified name of the referenced column is given
2. Analyze Query Requirements: 
    - Original Question: Consider what information the query is supposed to retrieve. 
    - Executed SQL Query: Review the SQL query that was previously executed and led to an error or incorrect result. 
    - Execution Result: Analyze the outcome of the executed query to identify why it failed (e.g., syntax errors, incorrect column references, logical mistakes). 
3. Correct the Query: 
    - Modify the SQL query to address the identified issues, ensuring it correctly fetches the requested data according to the database schema and query requirements.
    - For columns names with spaces, wrap them in backticks, e.g. "WHERE `car model` = 'bar'" instead of "WHERE car model = 'bar'".

**Output Format:** 
Present your corrected query as a single line of SQL code. 
Ensure there are no line breaks within the query.
Do not include any explanations, comments, or extra text.

Here are some examples: 

-------------------------------
Example 1:

Question:
 State the email of those who are staff of Murphy Diane whose number is 1002 and living in San Francisco staff of refers to reportsTO; San Francisco is a city;
 
Database Schema:
'[employees]':
  '[email]': text
  '[employeenumber]':
    primary_key: true
    type: integer
  '[firstname]': text
  '[lastname]': text
  '[officecode]':
    foreign_key: '[offices].[officecode]'
    type: text
  '[reportsto]':
    foreign_key: '[employees].[employeenumber]'
    type: integer
'[offices]':
  '[city]': text
  '[officecode]':
    primary_key: true
    type: text

The SQL query executed was:
SELECT [employees].[email] FROM [employees] INNER JOIN [offices] ON [employees].[officecode] = [offices].[officecode] WHERE [employees].[reportsto] = Murphy Diane AND [employees].[employeenumber] = 1002 AND [offices].[city] = San Francisco

The execution result: 
near "Diane": syntax error

Output:
SELECT T1.[email] FROM employees AS T1 JOIN offices AS T2 ON T1.[officecode] = T2.[officecode] WHERE T1.[reportsto] = 1002 AND T2.[city] = 'San Francisco'

-------------------------------
Example 2:
Question:
Among the German customers, how many of the them has credit limit of zero? German is a nationality of country = 'Germany'; CREDITLIMIT = 0

Database Schema:
'[customers]':
    '[country]': text
    '[creditlimit]': real
    '[customernumber]':
        primary_key: true
        type: integer

The SQL query executed was: 
SELECT COUNT(*) FROM [customers] WHERE [customers].[country] = 'German' AND [creditlimit] = 0

Output:
SELECT COUNT(*) FROM [customers] WHERE [customers].[country] = 'Germany' AND [creditlimit] = 0

The execution result: 
[]

-------------------------------
Example 3:
Question:
List the store located cities with regions in no water area of California state. cities refer to City Name; no water area refers to Water Area = 0;

Database Schema:
schema:
 '[regions]':
  '[region]': text
  '[state]': text
  '[statecode]':
    primary_key: true
    type: text
'[store locations]':
  '[city name]': text
  '[state]': text
  '[statecode]':
    foreign_key: '[regions].[statecode]'
    type: text
  '[water area]': integer
The SQL query executed was: 
SELECT T1.[city name], T2.[region] FROM store_locations AS T1 JOIN regions AS T2 ON T1.[statecode] = T2.[statecode] WHERE T2.[state] = 'California' AND T1.[water area] = 0

Output:
SELECT T1.[city name], T2.[region] FROM [Store Locations] AS T1 JOIN regions AS T2 ON T1.[statecode] = T2.[statecode] WHERE T2.[state] = 'California' AND T1.[water area] = 0

The execution result: 
no such table: store_locations

======= Your task ======= 
************************** 
Database schema:
{schema} 
************************** 
The original question is: 
Question: {question} 
SQL Query: {sql} 
************************** 
Based on the question, table schema and the previous query, analyze the result try to fix the query.
"""

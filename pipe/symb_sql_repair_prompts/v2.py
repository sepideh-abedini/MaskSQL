REPAIR_SYMBOLIC_SQL_PROMPT_V2 = """
You are an SQL database expert tasked with debugging a SQL query. 
A previous attempt to predict a SQL query given a masked NL question and DB schema did not yield the correct results in some cases, 
either due to errors in execution or because the result returned was empty or unexpected. 
Your task is to analyze the masked SQL query given the corresponding database schema and the NL question 
and fix any error in the query if it exists.
You should then provide a corrected version of the SQL query.
Note that there may be errors in how the NL question tokens were linked and masked with the database schema elements.
As a result, the masked SQL query might contain inaccuracies based on these incorrect mappings, 
and part of your task is to consider these issues as well.

**Procedure:** 
1. Review Database Schema: 
    - Examine the database schema to understand the database structure.
    - Database schema is given in YAML format where top-level keys are table names; each table lists its columns and their data types.
    - Each column might be primary key or a foreign key.
2. Analyze Query Requirements: 
    - NL Question: Consider what information the query is supposed to retrieve. 
    - Predicted SQL Query: Review the SQL query that was previously predicted and might led to error or incorrect result. 
3. Correct the Query: 
    - Modify the SQL query to address the identified issues, ensuring it correctly fetches the requested data according to the database schema and query requirements.
    
**Output Format:** 
Present your corrected query as a single line of SQL code. 
Ensure there are no line breaks within the query.
Do not include any explanations, comments, or extra text.

Here are some examples: 
The first two example had some errors and corrected version was returned.
The third example had no errors, so the exact same query is returned without any modification.

-------------------------------
Example 1:

NL Question:
List the [C2] of stores in the [V1] [T1] that are no water area. no water area refers to Water Area = 0; [V1] is a value of 
the column [T1].[C1].
  
Database Schema:
schema:
 '[T1]':
  '[C1]': text
  '[area]': text
  '[rid]':
    primary_key: true
    type: text
'[store]':
  '[C2]': text
  '[revenue]': integer
  '[rid]':
    foreign_key: '[T1].[rid]'
    type: text
  '[water area]': integer
  
The predicted SQL query was: 
SELECT [store].[C2] FROM [store] JOIN [T1] ON [T1].[rid] = [store].[rid] WHERE [T1].[C1] = '[V1]' AND [store][water area] = 'no';

The corrected SQL query is:
SELECT DISTINCT [store].[C2] FROM [store] JOIN [T1] ON [T1].[rid] = [store].[rid] WHERE [T1].[C1] = '[V1]' AND [store][water area] = 0;

-------------------------------
Example 2:

NL Question:
“Find the [C3] of [T1] who work in [T2] that are located in [V1]. [V1] is a value of the column [C5]
 
Database Schema:
'[T1]':
  '[C1]': text
  '[C2]':
    primary_key: true
    type: integer
  '[C3]': text
  '[C4]':
    foreign_key: '[T2].[C6]'
    type: text
'[T2]':
  '[C5]': text
  '[C6]':
    primary_key: true
    type: text

The predicted SQL query was: 
SELECT [T1].[C3] FROM [T1] WHERE [T1].[C5] = '[V1]';

The corrected SQL query is:
SELECT [T1].[C3] FROM [T1] JOIN [T2] ON [T1].[C4] = [T2].[C6] WHERE [T2].[C5] = '[V1]';

-------------------------------
Example 3:

NL Question:
Among the [V1] [T1], how many of the them has [C2] of zero? [V1] is a nationality of [C1] = [V1];

Database Schema:
'[T1]':
    '[C1]': text
    '[C2]': real
    '[C3]':
        primary_key: true
        type: integer

The predicted SQL query was: 
SELECT COUNT(*) FROM [T1] WHERE [T1].[C1] = '[V1]' AND [C2] = 0

The corrected SQL query is:
SELECT COUNT(*) FROM [T1] WHERE [T1].[C1] = '[V1]' AND [C2] = 0

======= Your task ======= 
************************** 
Database schema:
{schema} 
************************** 
The original question is: 
NL Question: {question} 
The predicted SQL query: {sql} 
************************** 
Based on the NL question, database schema and the previously predicted SQL query, 
analyze the query and question and fix the SQL query if needed.
"""

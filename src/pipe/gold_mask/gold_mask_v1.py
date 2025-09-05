GOLD_MASK_V1 = """
I'll give you a natural language question and the schema of the underlying database.
Your task is to mask every references to the database items in the given question.
Database items means columns or tables.
References to database have three types:
1- Tables: using the name of table or some term referencing a column 
2- Columns: using the name of a column or some term referencing a column
3- Literal Values: literal values that are related to database columns

Your goal is to find all such references and mask them using place holders. 
You should use [M1],[M2],... symbols to replace all such references.


Here are some examples:
-----------------------------------
Example 1:
Question:
Among the German customers, how many of the them has credit limit of zero? 

Database Schema:
'[customers]':
    '[country]': text
    '[creditlimit]': real
    '[customernumber]':
        primary_key: true
        type: integer

OUTPUT: 
Among the [M1] [M2], how many of them has [M3] of [M4]?  
-----------------------------------

Now, based on the given question and database schema returned the masked question:
Question: {question}
DB Schema: {schema}
"""

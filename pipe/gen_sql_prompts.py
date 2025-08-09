GEN_SQL_PROMPT_V1 = """
I give you a natural language question where I replaced some n-grams that reference a column name of the database 
with symbolic variables like [T1].[C1] for columns and [T1] for tables.
Each of these variables represents a database schema item. 
Schema items are also symbolic variables.
I will give the database schema based on these symbolic variables.
You should generate a symbolic SQL query that can be used to answer the question.
You should use the symbolic variables to generate the SQL query.

Example:
Symbolic Question: "What is the T1.C1 of the T1 who has the lowest T1.C2?"
Symbolic Schema:
   [T1]:
       [T1].[C1]: text
       [T2].[C2]: number
       [T2].[C3]:
           type: text
           foreign_key: [T2].[C4]
   [T2]:
        [T2].[C4]: text    
Symbolic SQL: "SELECT T1.C1 FROM T1 ORDER BY T1.C2 LIMIT 1"

Now give me the symbolic SQL query for the following data:
Symbolic Question: {symbolic_question}
Symbolic Schema: {symbolic_schema}

Go step by step but give the final answer wrapped in ``` ```
"""

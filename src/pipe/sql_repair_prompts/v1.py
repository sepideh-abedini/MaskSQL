REPAIR_SQL_PROMPT_V1 = """
I'll give you a natural language question, the schema of the underlying database, and a candidate SQL query.
Repair the given SQL and fix any errors to make it a valid SQL query that can be executed on the given database schema.

NL Question: {question}
Database Schema: {schema}
Candidate SQL: {sql}

Instructions: 
 - Your output should only contain the SQL query nothing else is permitted.
"""

SLM_MASK_PROMPT_V1 = """
You are a database expert. You are given:
- A natural language question 
- A database schema

Your goal is to rename all table and column names in the database schema to symbolic names.
You should use [C1],[C2],... for column names and [T1],[T2],... for table names and [V1],[V2],...
After renaming all database schema items, then you should also use these symbolic names in the question
and replace all references to the schema items with these symbolic names.
Then you should return the new symbolic question alongside the symbolic database schema.

Output Rules:
- For the literal values, append a string "[V1] is a value of [T1].[C1]" to the question
specifying that [V1] is related to the column [C1] of [T1].
- Do not include any extra information in the output like comments or extra explanation

Example:
NL Question: What is the release title of the music that was released by Ron Hunt in 1979 that was downloaded 239 times? 
Database Schema:
    songs:
        rt: text
        artist: text
        releasetype: text
        year: number
        totalsnatched: number

Output:
Symbolic Question: What is the [T1].[C1] of the [T1] that was released by [V1] in [V2] that was downloaded [V3] times?
[V1] is a value of [T1].[C2], [V2] is a value of [T1].[C4], [V3] is a value of [T1].[C5]
Symbolic Schema:
    [T1]:
        [C1]: text
        [C2]: text
        [C3]: text
        [C4]: number
        [C5]: number

Now generate the symbolic version of the following question and schema:
Question: {question}
DB Schema: {schema}
"""

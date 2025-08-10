SLM_UNMASK_PROMPT_V1 = """
You are a database expert. You are given
- A natural language question
- Masked version of the question
- A database schema
- Masked version of the database schema
- A masked SQL query

Your goal is to replace all masked tokens in the SQL query with their actual values.
Masked tokens include [C1],[C2],... for column names, [T1],[T2],... for table names, and [V1],[V2],... for literal 
values.
You should carefully inspect the original question and database schema and based on the masked versions 
find the proper mapping between mask tokens and actual values in order to restore the original SQL.
You should return only a single sql, nothing else is permitted.
Output Rules:
- No masked tokens should remain in the resulting SQL query
- Do not confuse table aliases with mask symbols
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

Masked Question: What is the [T1].[C1] of the [T1] that was released by [V1] in [V2] that was downloaded [V3] times?
[V1] is a value of [T1].[C2], [V2] is a value of [T1].[C4], [V3] is a value of [T1].[C5]
Masked Schema:
    [T1]:
        [C1]: text
        [C2]: text
        [C3]: text
        [C4]: number
        [C5]: number

Masked SQL:
SQL: SELECT [C1] FROM [T1] WHERE [C2] LIKE [V1] AND [C4] = [V2] AND [C5] = [V3]

Output:
SELECT rt FROM songs WHERE artist LIKE 'ron hunt' AND year = 1979 AND totalsnatched = 239

Now based on the given question, DB schema, their masked versions and the following masked SQL,
return the original SQL query:
Question: {question}
Schema: {schema}
{masked_raw}
Masked SQL: {masked_sql}
"""

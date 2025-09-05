MASKED_GEN_SQL_PROMPT_V2 = """
I'll give you a natural language question and the schema of the underlying database
Your task is to generate a SQL query that answers the question based on the database schema.
Database schema is given in yaml format. 

Here are some examples:

Example 1:
NL Question: What is the release title of the single that was released by Ron Hunt in 1979 that was downloaded 239 times? release title refers to groupName; Ron Hunt is an artist; groupYear = 1979; releaseType = 'single'; downloaded 239 times refer to totalSnatched = 239;
Database Schema:
    torrents:
        groupname: text
        artist: text
        releasetype: text
        groupyear: number
        totalsnatched: number
    tags:
        tag: text
        index: number
        id: number

SQL: SELECT groupName FROM torrents WHERE artist LIKE 'ron hunt & ronnie g & the sm crew' AND groupYear = 1979 AND releaseType LIKE 'single' AND totalSnatched = 239

Example 2:
NL Question: How many times was the album released by blowfly in 1980 downloaded? blowfly is an artist; groupYear = 1980; album refers to releaseType; downloaded refers to totalSnatched;
Database Schema:
    torrents:
        groupname: text
        artist: text
        releasetype: text
        groupyear: number
        totalsnatched: number
    tags:
        tag: text
        index: number
        id: number

SQL: SELECT totalSnatched FROM torrents WHERE artist LIKE 'blowfly' AND groupYear = 1980

Instructions:
- Use fully qualified column names in your SQL query. e.g., use [table_name].[column_name] instead of just [column_name].
- Do not include any additional text, explanations, or formatting.
- Do not include any comments.
- Output only the SQL query.

Now, generate a SQL query for the following question and database schema:
NL Question: {question}
Database Schema: {schema}
Your output should only contain the SQL query nothing else is permitted.
"""

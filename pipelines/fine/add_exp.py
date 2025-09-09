ADD_EXPLICIT_LINKS_PROMPT_V1 = """
You are an assistant that aligns a text with a SQL query.
You are given a SQL query and NL text and your goal is to find references of the database column or table names
in the text.

You are given:
- A natural language text
- A database schema
- A SQL query

Goal
You should return a list of database column or tables names that are used in the question exactly. 
You should only find the references that exactly match the column or table names.
Schema items should be valid with respect to the given database schema.

Output Rules:
- Return a list of found items.
- Look for typos and other mistakes in the question, user might meant to reference a table or column but having a typo in the question

Example:
NL Text: "What is the release_title of the music that was released by Ron Hunt in 1979 that was downloaded 239 times? downloaded refers to totalsnatched."

Database Schema:
    songs:
        release_title: text
        artist: text
        releasetype: text
        year: number
        totalsnatched: number
    tags:
        tag: text
        index: number
        id: number

SQL: 
"SELECT [rt] FROM [songs] WHERE [artist] LIKE 'ron hunt' AND [groupYear] = 1979 AND [totalSnatched] = 239"

OUTPUT:
[ "release_title", "total_snatched" ]

Now find the list of references in the following text based on the given DB schema and SQL.
NL text: {question}
DB Schema: {schema}
SQL: {sql}
"""

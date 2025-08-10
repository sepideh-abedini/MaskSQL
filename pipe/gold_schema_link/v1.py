GOLD_SCHEMA_LINKING_PROMPT_V1 = """
You are an assistant that links n-grams (sub-sequences of up to 3 consecutive words) 
of a natural-language question to database schema items (tables or fully qualified columns).

You are given:
- A natural language question.
- A database schema
- A SQL query

Goal
Return a JSON object mapping relevant n-grams (contiguous word sequences of length 1–3 taken from the question text) 
to the single most relevant schema item or a list of relevant schema items. 
You should look at the SQL query and extract the mapping between the question terms and database 
schema items.
The keys of the mapping are n-grams of the question and values should be a schema item.
Each schema item has one of the following forms:
- "TABLE:[table]": if n-gram references a table
- "COLUMN:[table].[column]": if n-gram references a column 
- "VALUE:[table].[column]": if n-gram is a literal value related to a column

Schema items should be valid with respect to the given database schema.

Mapping Rules:
- Consider all 1-, 2-, and 3-word spans.
- Include a mapping only if the n-gram refers to a schema item.
- Prefer the most specific applicable item: column beats table when the question refers to an attribute.
- Chose the shortest n-gram that maps to the schema item.
- If removing a word from an n-gram still points to the same schema item, use the shorter version.
- Exclude stop words from the n-grams

Output Rules:
- Output only a JSON object representing the mapping.
- Each entry should be a key-value pair where the key is an n-gram and the value is a schema item.
- Value of each entry can only be a single string of the form "COLUMN:[table].[column]" or "TABLE:[table]".
- All json key and values should be in double quotes.
- Output should be a top-level JSON object. No nested keys.

Example:
NL Question: What is the release title of the music that was released by Ron Hunt in 1979 that was downloaded 239 times? 
Database Schema:
    songs:
        rt: text
        artist: text
        releasetype: text
        year: number
        totalsnatched: number
    tags:
        tag: text
        index: number
        id: number

SQL: 
SELECT [rt] FROM [songs] WHERE [artist] LIKE 'ron hunt' AND [groupYear] = 1979 AND [totalSnatched] = 239

OUTPUT:
{{
    "release title": "COLUMN:[torrents].[rt]",
    "music": "TABLE:[songs]",
    "Ron Hunt": "COLUMN:[songs].[artist]",
    "1979": "VALUE:[songs].[year]",
    "downloaded": "COLUMN:[songs].[totalsnatched]"
    "239": "VALUE:[songs].[totalsnatched]"
}}

Now generate the JSON object of mapping for the following question and schema items:
Question: {question}
DB Schema: {schema}
SQL: {sql}
"""

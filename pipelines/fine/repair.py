GOLD_SCHEMA_LINKING_REPAIR_PROMPT_V1 = """
You are an assistant that aligns a text with a SQL query.
You are given a SQL query and NL text and your goal is to generate a mapping from 
n-gram of the text (sub-sequences of up to 3 consecutive words) 
to database schema items (tables, columns or literal values related to a column).

You are given:
- A natural language text
- A database schema
- A SQL query

Goal
You should return a JSON object mapping relevant n-grams (contiguous word sequences of length 1–3 taken from the question text) 
to the most relevant schema item or a list of relevant schema items. 
The keys of the mapping are n-grams of the text and values should be a schema item.
Each schema item has one of the following forms:
- "TABLE:[table]": if n-gram references a table
- "COLUMN:[table].[column]": if n-gram references a column 
- "VALUE:[table].[column]": if n-gram is a literal value related to a column

Instructions:
- Iterate through each word in the SQL and filter out anything that is not a schema item (SQL keywords or syntax punctuations)
- For each reference in the SQL find the most relevant n-gram in the text

Schema items should be valid with respect to the given database schema.

Mapping Rules:
- Consider all 1-, 2-, and 3-word spans.
- Include a mapping only if the n-gram refers to a schema item.
- Prefer the most specific applicable item: column beats table when the text refers to an attribute.
- Chose the shortest n-gram that maps to the schema item.
- If removing a word from an n-gram still points to the same schema item, use the shorter version.
- Exclude stop words from the n-grams
- There might be the exact same name of a column or table name in the text, so make sure they are included in the links.
- Some terms require to be combined with the adjacent words to be relative to a schema links
- Some terms might have redundant words such that removing them still allows the relation

Output Rules:
- Output only a JSON object representing the mapping.
- Each entry should be a key-value pair where the key is an n-gram and the value is a schema item.
- Value of each entry can only be a single string of the form "COLUMN:[table].[column]" or "TABLE:[table]".
- All json key and values should be in double quotes.
- Output should be a top-level JSON object. No nested keys.
- Each key of the final mapping should be exactly the same as it appears in the text

Example:
NL Text: What is the release title of the music that was released by Ron Hunt in 1979 that was downloaded 239 times? 
downloaded refers to  
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

Now repair the given dictionary of schema links based on the following text, database schema, and SQL query:
NL text: {question}
DB Schema: {schema}
SQL: {sql}
"""

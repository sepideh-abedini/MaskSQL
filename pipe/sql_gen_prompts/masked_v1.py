GEN_SQL_PROMPT_V1 = """
I'll give you a natural language question and the schema of the underlying database.
Your task is to generate a SQL query that answers the question based on the database schema.

I don't provide the full database schema. Instead I only provide a schema linking for the most relevant terms in the question.
The schema linking is sorted in descending order of relevance to the question.
The first 4 schema linking items are the most relevant schema linking items.
So, the first 4 schema linking items are the most relevant schema linking items.
Note that there might be schema linking items that are not relevant to the question but included in the schema linking because
we always pick top 4 schema linking items.. 
Each schema item is of the form table_name.column_name of the underlying database.
Schema items are sorted in descending order of relevance to the question. 
First we sort the most relevant tables and then we sort the most relevant columns within each table.
We include the top 4 tables and top 5 columns within each table.
So, we include the columns of the first table (the most relevant table), followed by the columns of the second table
and so on. Columns of the first table are sorted in descending order of relevance to the question.
Note that there might be tables or columns that are not relevant to the question but included in the schema items because
we always pick top 4 tables and top 5 columns within each table.

Additionally, I provide you with a list of schema linking items. 
Each schema linking item is a mapping from an schema item to an n-gram in the question that references the schema item.
Each item has the following format.
'table_name.column_name="n-gram in the question that references the schema item"'
I don't provide the full database schema. Instead I only provide a schema linking for the most relevant terms in the question.

Here are some examples:
Example 1:
NL Question: What is the release title of the single that was released by Ron Hunt in 1979 that was downloaded 239 times? release title refers to groupName; Ron Hunt is an artist; groupYear = 1979; releaseType = 'single'; downloaded 239 times refer to totalSnatched = 239;
SchemaItems:
    - torrents.groupname
    - torrents.artist
    - torrents.releasetype
    - torrents.groupyear
    - torrents.totalsnatched
    - tags.tag
    - tags.index
    - tags.id

SQL: SELECT groupName FROM torrents WHERE artist LIKE 'ron hunt & ronnie g & the sm crew' AND groupYear = 1979 AND releaseType LIKE 'single' AND totalSnatched = 239

Example 2:
NL Question: How many times was the album released by blowfly in 1980 downloaded? blowfly is an artist; groupYear = 1980; album refers to releaseType; downloaded refers to totalSnatched;
SchemaItems:
    - torrents.totalsnatched
    - torrents.artist
    - torrents.groupyear
    - torrents.releasetype
    - torrents.groupname
    - tags.tag
    - tags.index
    - tags.id

SQL: SELECT totalSnatched FROM torrents WHERE artist LIKE 'blowfly' AND groupYear = 1980

Now, generate a SQL query for the following question and database schema:
NL Question: {question}
SchemaItems: {schema_items}
Your output should only contain the SQL query nothing else is permitted.
"""

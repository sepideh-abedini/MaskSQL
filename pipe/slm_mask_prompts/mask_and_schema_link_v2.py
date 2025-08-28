SLM_MASK_AND_LINK_PROMPT_V2 = """
You are a database expert. 
Inputs:
- A natural language text 
- A database schema
- A symbol lookup table
- Value links

Your goal is to mask all references to database items in the text with special symbols given in the symbol lookup table.
You should not change structure of the text or rephrase anything. 
You should only replace references to database (table name, column name, or a literal value referencing a value of a column) with the given symbols. 

The symbol lookup table is a mapping from schema items to their corresponding symbol that should be used for masking.
[C1],[C2],... are for column names, [T1],[T2],... are for table names. 
For literal values you should use the given value links that maps terms in the question with their related database column.

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

Symbol Table:
{{
    "[songs]": "[T1]",
    "[songs].[rt]": "[C1]",
    "[songs].[artist]": "[C2]",
    "[songs].[releasetype]": "[C3]",
    "[songs].[year]": "[C4]",
    "[songs].[totalsnatched]": "[C5]",
}}

Value Links:
{{
    "Ron Hunt": "[songs].[artist]",
    "1979": "[songs].[year]",
    "239": "[songs].[totalsnatched]"
}}

Output:
`What is the [T1].[C1] of the [T1] that was released by [V1] in [V2] that was downloaded [V3] times?
[V1] is a value of [T1].[C2], [V2] is a value of [T1].[C4], [V3] is a value of [T1].[C5]`

Now generate the masked version of the following question:
Question: {question}
DB Schema: {schema}
Value Links: {value_links}
Symbol Table: {symbol_table}
"""

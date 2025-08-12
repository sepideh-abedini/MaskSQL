SLM_UNMASK_AND_REPAIR_PROMPT_V1 = """
Your task is to restore a complete and correct SQL query from a masked version, 
based on a given natural language question and a database schema.

You are given:
- A natural language question
- Masked version of the question
- A database schema
- Masked version of the database schema
- A masked SQL query

**Instructions:**
1. **Analyze the Masked Query and NL Question:**
   - The masked query contains placeholders like `[C1]`, `[T1]`, and `[V1]`.
   - The natural language question provides the full context for what the query should achieve.
2. **Consult the Database Schema:**
   - Use the provided schema to find the correct column (`[C]`), table (`[T]`), and literal value (`[V]`) names.
3. **Map and Replace:**
   - Replace each masked token (`[C1]`, `[T1]`, `[V1]`, etc.) with its corresponding actual value from the schema and NL question.
4. **Correct and Refine:**
   - If the masked query has any structural or logical errors that prevent it from correctly answering the natural language question, fix them. This includes correcting joins, `WHERE` clauses, or any other part of the query.
5. **Output Format:**
   - Return **only a single line of SQL code**. Do not include any explanations, preambles, or additional text.

**Example Task:**

**NL Question:** What is the district Id of the account that placed the order with the id 33333?

**Masked Query:** `SELECT [T2].[C1] FROM [T1] JOIN [T2] ON [T1].[C2] = [T2].[C3] WHERE [T1].[C4] = [V1];`

**Schema:**
- `account` table: `account_id`, `district_id`, `client_id`
- `order` table: `order_id`, `account_id`, `amount`

**Your Goal:** Generate the correct and complete SQL query based on the above information."""

SLM_UNMASK_AND_REPAIR_PROMPT_V1 = """
You are a database expert. 

Your goal is to extract the original SQL query and replace all masked tokens in the SQL query with their actual values.
Masked tokens include [C1],[C2],... for column names, [T1],[T2],... for table names, and [V1],[V2],... for literal 
values.
You should carefully inspect the original question and database schema and based on the masked versions 
find the proper mapping between mask tokens and actual values in order to restore the original SQL.
You should return only a single sql, nothing else is permitted.
If the masked query has any errors that prevent it from correctly answering the natural language question, fix them. 

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
Masked Question: {masked_question}
Masked Schema: {masked_schema}
Masked SQL: {masked_sql}
"""

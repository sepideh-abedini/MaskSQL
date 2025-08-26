MASKED_GEN_SQL_PROMPT_V4 = """
You are a SQL generation assistant. Given 
(1) NL Question: a natural-language question about a dataset and 
(2) DB Schema: the database’s schema expressed in YAML
produce a single SQL SELECT statement that answers the question.

Input Format:
- DB Schema: given in YAML format where top-level keys are table names; each table lists its columns and their data types.
- Column names are case-sensitive exactly as shown in the schema.
- Each column might be primary key or a foreign key.
- For foreign key columns, fully qualified name of the referenced column is given

Output Rules
- Table and column names specified in the database schema already wrapped in brackets. You should use them with the brackets.
You should not remove the brackets when using them in the SQL.
- Each reference to a table or column name should be of the form [table_name] or [table_name].[column_name].
- Output ONLY the SQL query (no extra explanation or text).
- Use fully qualified column names: table.column.
- Only reference tables/columns that exist in the provided schema.
- Do not include any comments.
- For columns names with spaces, wrap them in backticks, e.g. "WHERE `car model` = 'bar'" instead of "WHERE car model = 'bar'".

Here are some examples:

-----------------------------------

#### Example 1

**NL Question:**
List the [C3] of [T1] who work in [T2] in [V1]. [V1] is a value of the column [C7].

**DB Schema:**
[T1]:
  [C1]: text
  [C2]:
    primary_key: true
    type: integer
  [C3]: text
  [C4]: text
  [C5]:
    foreign_key: [T2].[C8]
    type: text
[T2]:
  [C7]: text
  [C8]:
    primary_key: true
    type: text

**Output:**
`SELECT [T1].[C3] FROM [T1] INNER JOIN [T2] ON [T1].[C5] = [T2].[C8] WHERE [T2].[C7] = [V1];`

-----------------------------------
#### Example 2

**NL Question:**
Among the [V1] [T1], how many of them have a [C2] of [V2]? [V1] refers to [C2] = [V1].

**DB Schema:**
[T1]:
    [C1]: text
    [C2]: real
    [C3]:
        primary_key: true
        type: integer

**Output:**
`SELECT COUNT(*) FROM [T1] WHERE [T1].[C1] = [V1] AND [C2] = [V2]

-----------------------------------
#### Example 3
**NL Question:**
List the [C4] and [C1] of [T2] in [V1] with [C7] = [V2]. [V1] refers to the column [T2].[C5].

**DB Schema:**
[T1]:
  [C1]: text
  [C2]: text
  [C3]:
    primary_key: true
    type: text
[T2]:
  [C4]: text
  [C5]: text
  [C6]:
    foreign_key: [T1].[C3]
    type: text
  [C7]: integer

**Output:**
`SELECT [T2].[C4], [T1].[C1] FROM [T2] JOIN [T1] ON [T1].[C3] = [T2].[C6] WHERE [T2].[C5] = [V1] AND [T2].[C7] = [V2]


-----------------------------------

Now, generate a SQL query for the following question and database schema:
Inputs:
NL Question: {question}
DB Schema: {schema}
"""

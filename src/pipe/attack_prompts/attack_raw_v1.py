ATTACK_PROMPT_RAW_V1 = """
Your goal is to guess the words in a masked question. Given 
(1) NL Question: a natural-language question about a dataset and 
(2) DB Schema: the database’s schema expressed in YAML
guess the original each masked symbol exists in the question.
Masked symbols are wrapped in brackets.

Input Format:
- DB Schema: given in YAML format where top-level keys are table names; each table lists its columns and their data types.
- Each column might be primary key or a foreign key.
- For foreign key columns, fully qualified name of the referenced column is given

Output Rules
- C1,C2,... are symbols used to mask column names.
- T1,T2,... are symbols used to mask table names.
- V1,V2,... are symbols used to mask literal values.
- Output ONLY the unmasked question.
- Do not include any comments.
- For columns names with spaces, wrap them in backticks, e.g. "WHERE `car model` = 'bar'" instead of "WHERE car model = 'bar'".

Here are some examples:

-----------------------------------
Example 1:
NL Question: What is the [T1].[C1] of [T1] who have a [T2] with [T2].[C4] higher than [V1]? [V1] is a value of [T2].[C4]
Database Schema:
    [T1]:
        [C1]: text
        [C2]: text
    [T2]:
        [C3]: text
        [C4]: number

OUTPUT: 
What is the name of people who have a car with horse power higher than 1000?

Now, unmask the following question considering the following DB schema
Inputs:
{symbolic_raw}
"""

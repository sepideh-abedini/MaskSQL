ATTACK_PROMPT_V2 = """
Your goal is to guess the words in a masked text. Given 
(1) NL text: a natural-language text explaining instruction to extract information from 
a database 
(2) DB Schema: the database’s schema expressed in YAML
guess the original each masked symbol exists in the text.
Masked symbols are wrapped in brackets.

Input Format:
- DB Schema: given in YAML format where top-level keys are table names; each table lists its columns and their data types.
- Each column might be primary key or a foreign key.
- For foreign key columns, fully qualified name of the referenced column is given

Output Rules
- C1,C2,... are symbols used to mask column names.
- T1,T2,... are symbols used to mask table names.
- V1,V2,... are symbols used to mask literal values.
- Output ONLY the unmasked text.
- The output should contain all of the unmasked tokens in the text, no portion of text should be omitted
- Do not include any comments.
- For columns names with spaces, wrap them in backticks, e.g. "WHERE `car model` = 'bar'" instead of "WHERE car model = 'bar'".

Here are some examples:

-----------------------------------
Example 1:
NL Text: What is the [T1].[C1] of [T1] who have a [T2] with [T2].[C4] higher than [V1]? [V1] is a value of [T2].[C4]
Database Schema:
    [T1]:
        [C1]: text
        [C2]: text
    [T2]:
        [C3]: text
        [C4]: number

OUTPUT: 
What is the name of people who have a car with horse power higher than 1000? 1000 is a value of horse power

Now, unmask the following text considering the following DB schema
Inputs:
NL Text: {question}
DB Schema: {schema}
"""

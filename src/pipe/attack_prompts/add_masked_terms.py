ADD_MASKED_TERMS_PROMPT_V1 = """
You are given a text in its masked version, your goal is to return a mapping from 
each unmasked n-grams in the original text to their masked symbol in the masked text.
Masked symbols are wrapped in [] for instance [C1] or [T1].[C1].
You should consider [T1].[C1] as a single symbol.
You should return a json object with keys being terms in the original text and values being 
symbols used in the masked text.
Do not include any comments or extra text in the output. 
Output should be a valid json object.

Here are some examples:

-----------------------------------
Example 1:
Text: What is the name of people who have a car with horse power higher than 1000?
Masked Text: What is the [T1].[C1] of [T1] who have a [T2] with [T2].[C4] higher than [V1]? [V1] is a value of [T2].[C4]
OUTPUT: 
{{
    "name": "[T1].[C1]",
    "people": "[T1]",
    "car": "[T2]",
    "horse power": "[T2].[C4]",
    "1000": "[V1]"
}}

Now, return the mapping for the following text and its masked version:
Inputs:
Text: {question}
Masked Text: {masked_question}
"""

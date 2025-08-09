import re

from RESDSQL.pipeline_stage import PipelineStage

PROMPT = """
I give a natural language question and a list SchemaItems that includes database table_name.column_names ranked by their relevance to the given NL question.
I also give you alist SchemaLinks that includes a list of mappings from schema items to n-grams in the question.
Now based on the given SchemaLinks, for each term that has a mapping, replace it with the index of the item in the SchemaItems list.
We call the question foobared after the replacements. 

Example:
NL Question: "What is the name of the instructor who has the lowest salary?"
SchemaItems: ["instructor.name", "instructor.salary", "department.name"]
SchemaLinks: ['instructor.name="the name of the instructor"', 'instructor.salary="salary"']
Foobared NL Question: "What is [0] who has the lowest [1]?

Give me the foobared NL question for the following data:
NL Question: {question}
SchemaItems: {sitems}
SchemaLinks: {slinks}

Go step by step but give the final answer wrapped in ``` ```
"""


class MaskQuestion(PipelineStage):
    def process_output(self, output):
        masked = re.findall(r"```([\s\S]*?)```", output)
        final_answer = masked[0]
        final_answer = final_answer.strip()
        return final_answer

    def get_prompt(self, row):
        slinks = row['schema_links']
        sitems = row['schema_items']
        question = row['question']
        prompt = PROMPT.format(question=question, sitems=sitems, slinks=slinks)
        return prompt

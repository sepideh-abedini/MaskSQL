import re

from RESDSQL.pipeline_stage import PipelineStage

PROMPT = """
I give you a natural language question and a database schema.
Give me the SQL that can answer the given question.

Example:
NL Question: "What is the name of the instructor who has the lowest salary?"
DB Schema: 
tables:
    instructor:
       - id: text
       - name: text
       - dept_name: text
       - salary: number
   department:
       - dept_name: text
       - building: text
       - budget: number
       
SQL: "SELECT name FROM instructor ORDER BY salary LIMIT 1"

Now generate the SQL for the following data:
NL Question: {question}
DB Schema: {schema}
"""

N = 3


class EstimateSQL(PipelineStage):
    def process_output(self, output):
        masked = re.findall(r"```([\s\S]*?)```", output)
        final_answer = masked[0]
        final_answer = final_answer.strip()
        final_answer = final_answer.replace("\n", " ")
        if final_answer.startswith("sql"):
            final_answer = final_answer[3:]
        return final_answer

    def get_prompt(self, row):
        schema = row['schema']
        question = row['question']
        prompt = PROMPT.format(question=question, schema=schema)
        return prompt

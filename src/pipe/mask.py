import argparse
import asyncio
import json
import os
import re
from typing import List

import tqdm.asyncio as tqdm
from openai import AsyncClient
from pydantic import BaseModel

from RESDSQL.llm_util import send_prompt

DATA_DIR = "data"



async def gen():
    with open("resdsql_test.json") as f:
        data = json.load(f)

    prompts_file = open("out/mask_prompts.txt", "w")
    responses_file = open("out/mask_res.txt", "w")
    masked_data = []
    for i, row in enumerate(data):
        slinks = row['schema_links']
        sitems = row['tc_original']
        question = row['question']
        prompt = PROMPT.format(question=question, sitems=sitems, slinks=slinks)
        res = await send_prompt(prompt)
        masked = re.findall(r"```([\s\S]*?)```", res)
        final_answer = masked[0]
        final_answer = final_answer.strip()
        prompts_file.write(prompt + "\n")
        responses_file.write(res + "\n")
        row['masked_question'] = final_answer
        masked_data.append(row)

    prompts_file.close()
    responses_file.close()

    with open("out/masked_input.json", "w") as f:
        f.write(json.dumps(masked_data, indent=4))


async def main():
    await gen()


if __name__ == '__main__':
    asyncio.run(main())

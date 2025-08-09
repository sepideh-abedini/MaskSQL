import json
import os
import re
from typing import Tuple

from loguru import logger
from openai import AsyncClient


async def send_prompt(prompt, model=os.getenv("OPENAI_MODEL")) -> Tuple[str, str]:
    client = AsyncClient(
        organization=os.getenv("OPENAI_GROUP_ID"),
        project=os.getenv("OPENAI_PROJ_ID"),
        timeout=int(os.getenv("OPENAI_TIMEOUT", 60))
    )
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    if response.choices is None:
        print(prompt)
        raise Exception(f"LM prompt failed: {response.model_extra}")
    usage = 0
    if response.usage:
        usage = response.usage.total_tokens
    return response.choices[0].message.content, usage


def extract_json(text: str):
    try:
        if "```json" in text:
            res = re.findall(r"```json([\s\S]*?)```", text)
            json_res = json.loads(res[0])
        elif "```" in text:
            res = re.findall(r"```([\s\S]*?)```", text)
            json_res = json.loads(res[0])
        else:
            json_res = json.loads(text)
        return json_res
    except Exception as e:
        logger.error(f"Failed to extract json from: {text}, error={e}")
        return {}

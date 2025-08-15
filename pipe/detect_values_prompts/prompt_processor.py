import os
import time
from abc import abstractmethod
from json import JSONDecodeError

from loguru import logger

from pipe.llm_util import send_prompt
from pipe.processor.list_transformer import JsonListTransformer


class PromptProcessor(JsonListTransformer):
    def __init__(self, prop_name, model=os.environ['OPENAI_MODEL'], force=False):
        super().__init__(force)
        self.model = model
        self.prop_name = prop_name
        self.prompt_file = "/dev/null"
        self.response_file = "/dev/null"

    async def _prompt_llm(self, row, prompt: str):
        try:
            res, toks = await send_prompt(prompt, model=self.model)
        except JSONDecodeError as e:
            logger.error(f"Sending prompt failed: {e}")
            return "", 0
        except Exception as e:
            logger.error(f"Sending prompt failed: {e}")
            raise e
        processed_res = self._process_output(row, res)
        return processed_res, toks

    @abstractmethod
    def _process_output(self, row, output):
        pass

    @abstractmethod
    def _get_prompt(self, row):
        pass

    async def _process_row(self, row):
        prompt = self._get_prompt(row)
        with open(self.prompt_file, "a") as f:
            f.write(f"######################\n {prompt}\n")
        row['created'] = int(time.time())
        res, toks = await self._prompt_llm(row, prompt)
        row['finished'] = int(time.time())
        row['toks'] = toks
        with open(self.response_file, "a") as f:
            f.write(f"######################\n {res}\n")
        # row['total_toks'] += toks
        if self.prop_name in row:
            row[self.prop_name].update(res)
        else:
            row[self.prop_name] = res
        return row

    async def run(self, input_file):
        self.prompt_file = f"logs/{self.name}.prompt.txt"
        self.response_file = f"logs/{self.name}.response.txt"
        open(self.prompt_file, "w").close()
        open(self.response_file, "w").close()
        output_file = await super().run(input_file)
        return output_file

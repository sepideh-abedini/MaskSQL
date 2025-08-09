import json
import os
from abc import ABC, abstractmethod

import tqdm
from loguru import logger

from pipe.async_utils import apply_async
from pipe.processor.list_processor import JsonListProcessor

FORCE = int(os.environ.get("FORCE", 0)) > 0


class JsonListTransformer(JsonListProcessor, ABC):
    def __init__(self, force=True):
        self.force = force or FORCE

    def get_output_file(self, input_file):
        file_name = os.path.basename(input_file)
        dir_path = os.path.dirname(input_file)
        num = int(file_name.split("_", 1)[0])
        return os.path.join(dir_path, f"{num + 1}_{self.name}.json")

    async def run(self, input_file):
        output_file = self.get_output_file(input_file)

        if not self.force and os.path.exists(output_file):
            logger.debug(f"File exists: {output_file}, skipping.")
            return output_file

        updated_rows = await super().run(input_file)

        # updated_rows = []
        # for i, row in enumerate(self._get_input_data(input_file)):
        #     if self.prop_name in row:
        #         prop = row[self.prop_name]
        #         if isinstance(prop, dict):
        #             row[self.prop_name].update(output[i])
        #         elif isinstance(prop, int):
        #             row[self.prop_name] += int(output[i])
        #         else:
        #             raise Exception(f"Invalid prop type being updated: {self.prop_name}, {type(prop)}")
        #     else:
        #         row[self.prop_name] = output[i]
        #     updated_rows.append(row)

        with open(output_file, "w") as f:
            f.write(json.dumps(updated_rows, indent=4))
        return output_file

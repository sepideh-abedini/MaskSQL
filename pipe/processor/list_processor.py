import json
from abc import ABC, abstractmethod
from typing import Dict

from pipe.async_utils import apply_async


class JsonListProcessor(ABC):
    @abstractmethod
    async def _process_row(self, row: Dict) -> Dict:
        pass

    def get_prop(self, row, prop):
        props = prop.split(".")
        d = row
        for p in props:
            d = d[p]
        return d

    def set_prop(self, row, prop, value):
        props = prop.split(".")
        d = row
        for p in props[:-1]:
            d = d[p]
        d[props[-1]] = value
        return row

    @property
    def name(self):
        return self.__class__.__name__

    def _pre_run(self):
        pass

    def _post_run(self):
        pass

    def _get_input_data(self, input_file):
        with open(input_file) as f:
            in_data = json.load(f)
            return in_data

    async def run(self, input_file):
        in_data = self._get_input_data(input_file)

        output = await apply_async(self._process_row, in_data, self.name)

        self._post_run()

        return output

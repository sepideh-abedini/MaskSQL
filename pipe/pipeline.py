from typing import List

from loguru import logger

from pipe.monitor.lib import Timer
from pipe.monitor.mem import track_memory_async
from pipe.processor.list_processor import JsonListProcessor


class Pipeline:
    def __init__(self, stages: List[JsonListProcessor]):
        self.stages = stages

    async def __run_internal(self, input_file):
        tmp_file = input_file
        timer = Timer()
        timer.start()
        for stage in self.stages:
            print(f"Starting Stage: {stage.name}")
            tmp_file = await stage.run(tmp_file)
            print(f"Done Stage: {stage.name}, time={timer.lap()}")
        return tmp_file

    async def run(self, input_file):
        timer = Timer.start()
        _, avg_mem, peak_mem = await track_memory_async(self.__run_internal, input_file)
        total_time = timer.lap()
        # logger.info(f"TOTAL PRED TIME: {total_time}")
        # logger.info(f"AVG MEM: {avg_mem}")
        # logger.info(f"PEAK MEM: {peak_mem}")

import datetime
import math
import subprocess
from datetime import datetime

import pandas as pd
from loguru import logger


class TimeLogger:
    idx: str

    def __init__(self, idx: str):
        self.idx = idx

    @staticmethod
    def start(idx: str):
        timer = TimeLogger(idx)
        # logger.info(f"started", idx=f"{idx}", start=True)
        return timer

    def lap(self):
        pass
        # logger.info(f"finished", idx=f"{self.idx}", finish=True)


class Timer:
    start_time: datetime

    def __init__(self):
        self.start_time = datetime.now()

    @staticmethod
    def start():
        return Timer()

    def lap(self) -> float:
        return (datetime.now() - self.start_time).total_seconds()


def confidence_interval(column: pd.Series) -> str:
    if not pd.api.types.is_numeric_dtype(column):
        return "NA"
    CONFIDENCE = 0.95
    Z = 1.65
    SE = column.std() / math.sqrt(column.size)
    err_margin = Z * SE
    mean = column.mean()
    interval_start = mean - err_margin
    interval_end = mean + err_margin
    if interval_start >= 0 and interval_end <= 1 and interval_start >= 0 and interval_end <= 1:
        return "({:.2f}%, {:.2f}%)".format(interval_start * 100, interval_end * 100)
    else:
        return "({:.2f}, {:.2f})".format(interval_start * 100, interval_end * 100)
    # return f"({interval_start}, {interval_end})"


def execute_command(command: str):
    with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
        output, errors = p.communicate()
        print(output, errors)
    if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, p.args)

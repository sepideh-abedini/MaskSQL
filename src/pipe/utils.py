import re
from datetime import datetime

from loguru import logger


def replace_str(text: str, src: str, dst: str) -> str:
    try:
        result = re.sub(
            r"\b{}\b".format(re.escape(src)),
            dst,
            text,
            flags=re.IGNORECASE
        )
    except Exception as e:
        logger.error(f"Failed to replace {src} -> {dst} in {text}")
        result = text
    return result


def check_str(text: str, src: str) -> bool:
    try:
        pattern = r"\b{}\b".format(re.escape(src))
        if re.search(pattern, text, flags=re.IGNORECASE):
            return True
    except Exception as e:
        logger.error(f"Failed to search {src} in {text}")
    return False


def replace_str_punc(text: str, src: str, dst: str) -> str:
    try:
        result = re.sub(
            r'(?<![\w.]){}(?!\w)'.format(re.escape(src)),
            dst,
            text,
            flags=re.IGNORECASE
        )
    except Exception as e:
        logger.error(f"Failed to replace {src} -> {dst} in {text}")
        result = text
    return result


def check_str_punc(text: str, src: str) -> bool:
    try:
        pattern = r'(?<![\w.]){}(?!\w)'.format(re.escape(src))
        if re.search(pattern, text, flags=re.IGNORECASE):
            return True
    except Exception as e:
        logger.error(f"Failed to search {src} in {text}")
    return False


class Timer:
    start_time: datetime

    def __init__(self):
        self.start_time = datetime.now()

    @staticmethod
    def start():
        return Timer()

    def lap(self) -> float:
        return (datetime.now() - self.start_time).total_seconds()

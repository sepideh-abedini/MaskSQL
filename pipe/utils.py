import re

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

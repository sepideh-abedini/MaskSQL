import os
import sys

from loguru import logger

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


def configure_logging():
    try:
        logger.remove(0)
    except Exception:
        pass
    logger.add(sys.stderr, level=LOG_LEVEL, colorize=True, enqueue=True,
               format="<green>{time:HH:mm:ss}[{process.id}] | </green><level> {level}: {message}</level>")

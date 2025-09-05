import os
import threading
import time

import psutil
from loguru import logger


def _monitor_memory(interval: float, stop_event: threading.Event, mem_usage: list):
    process = psutil.Process(os.getpid())
    while not stop_event.is_set():
        rss = process.memory_info().rss / (1024 * 1024)
        logger.debug(f"Monitoring memory: {rss}")
        mem_usage.append(rss)
        time.sleep(interval)


async def track_memory_async(coro, *args, interval: float = 1, **kwargs):
    mem_usage = []
    stop_event = threading.Event()
    monitor_thread = threading.Thread(target=_monitor_memory, args=(interval, stop_event, mem_usage))
    monitor_thread.start()

    try:
        result = await coro(*args, **kwargs)
    finally:
        stop_event.set()
        monitor_thread.join()

    avg_mem = sum(mem_usage) / len(mem_usage) if mem_usage else 0
    peak_mem = max(mem_usage) if mem_usage else 0
    # print("MEM USAGE LEN: ", len(mem_usage))
    # print("MEM USAGE SUM: ", sum(mem_usage))
    return result, avg_mem, peak_mem

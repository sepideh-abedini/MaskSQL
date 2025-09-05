import asyncio
import os

from tqdm.asyncio import tqdm

ASYNC_BATCH = int(os.environ.get("ASYNC_BATCH", 1))


async def apply_async(fun, items, desc=""):
    semaphore = asyncio.Semaphore(ASYNC_BATCH)

    async def sem_task(item):
        async with semaphore:
            return await fun(item)

    tasks = [asyncio.create_task(sem_task(item)) for item in items]
    results = await tqdm.gather(*tasks, total=len(items), desc=desc)
    return results

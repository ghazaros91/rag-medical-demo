import asyncio
import logging
import random
from config import MAX_RETRIES, BACKOFF, TIMEOUT

class Reliability:
    @staticmethod
    async def with_retries(coro_fn):
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                return await asyncio.wait_for(coro_fn(), timeout=TIMEOUT)
            except Exception as e:
                logging.warning(f"Attempt {attempt}: {e}")
                if attempt == MAX_RETRIES:
                    raise
                await asyncio.sleep(BACKOFF * attempt + random.random())
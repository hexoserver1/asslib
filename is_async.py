import asyncio


def is_async(func):
    # Wrapper for asyncio.iscoroutine
    return asyncio.iscoroutinefunction(func) or asyncio.iscoroutine(func)

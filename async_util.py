import asyncio


def is_async(func):
    # Wrapper for asyncio.iscoroutine
    return asyncio.iscoroutinefunction(func) or asyncio.iscoroutine(func)


async def call(func, *args, **kwargs):
    # No more await mistakes!
    if is_async(func):
        return await func(*args, **kwargs)
    else:
        return func(*args, **kwargs)
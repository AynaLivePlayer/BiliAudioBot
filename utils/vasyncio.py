from functools import wraps


def asyncwrapper(func):
    @wraps(func)
    async def wrapper(*args,**kwargs):
        func(*args,**kwargs)
    return wrapper
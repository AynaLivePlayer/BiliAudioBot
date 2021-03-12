import traceback
from functools import wraps
import requests,asyncio

def asyncwrapper(func):
    @wraps(func)
    async def wrapper(*args,**kwargs):
        func(*args,**kwargs)
    return wrapper



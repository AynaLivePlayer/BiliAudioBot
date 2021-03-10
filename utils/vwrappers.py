from functools import wraps
import traceback

def TryExceptRetNone(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except:
            traceback.print_exc()
            return None
    return wrapper
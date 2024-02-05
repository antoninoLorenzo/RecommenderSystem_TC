import inspect
import functools
from abc import ABC, abstractmethod


class Item(ABC):
    pass

def not_none(*param_names):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            bound_args = inspect.signature(func).bind(*args, **kwargs).arguments
            for param_name in param_names:
                if param_name in bound_args and bound_args[param_name] is None:
                    raise ValueError(f"Parameter '{param_name}' cannot be None")
            return func(*args, **kwargs)
        return wrapper
    return decorator
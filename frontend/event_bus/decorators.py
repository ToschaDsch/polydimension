# decorators.py
from datetime import time

import time
import functools


def subscribe(func):
    func._subscribe = True
    return func


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        duration = end_time - start_time
        print(f"function {func.__name__!r} tine {duration:.4f}c.")
        return result

    return wrapper
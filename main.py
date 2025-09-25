import time
import re

def time_function(func):
    start = time.perf_counter()
    result = func()
    end = time.perf_counter()
    print(result)
    print(f"Execution time: {end - start:.4f} seconds")


time_function(func)
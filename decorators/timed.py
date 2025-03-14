"""
Module providing a decorator for measuring function execution time.

This module defines the `timed` decorator, which measures the execution time of a function 
and displays it in seconds or minutes, depending on the duration.
"""

import time

def timed(func):
    """Decorator measuring the time of performing the function."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time

        if elapsed_time < 60:
            print(f"\nDownload time: {elapsed_time:.2f} seconds.")
        else:
            print(f"\nDownload time: {elapsed_time / 60:.2f} minutes.")

        return result
    return wrapper

import time

def timed(func):
    """Decorator measuring the time of performing the function."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = (end_time - start_time) / 60
        print(f"\nDownload time: {elapsed_time:.2f} minutes.")
        return result
    return wrapper

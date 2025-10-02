import time
from fastapi import Request

async def timed_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    elapsed = time.time() - start_time
    print(f"Request {request.url.path} took {elapsed:.2f}s")
    return response
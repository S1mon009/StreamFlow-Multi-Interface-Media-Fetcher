from fastapi import Request
from fastapi.responses import JSONResponse
import socket


def is_connected(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
        return True
    except (socket.timeout, socket.error):
        return False


async def network_middleware(request: Request, call_next):
    if not is_connected():
        return JSONResponse(
            status_code=503,
            content={"detail": "No network connection. Please try again later."}
        )
    response = await call_next(request)
    return response
from fastapi import FastAPI
from routes.download import router
from middlewares.network_required import network_middleware
from middlewares.timed import timed_middleware


app = FastAPI(title="YouTube Video Downloader API", version="1.0")

app.middleware("http")(network_middleware)
app.middleware("http")(timed_middleware)

app.include_router(router, prefix="/api", tags=["Downloader"])

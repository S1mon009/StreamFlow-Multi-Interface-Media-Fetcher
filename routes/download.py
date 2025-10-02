import subprocess
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from schemas.download_schema import DownloadRequest
from decorators.ffmpeg import ffmpeg_required


router = APIRouter()


@router.post("/stream")
@ffmpeg_required
def stream_video(request: DownloadRequest):
    if not request.urls:
        raise HTTPException(status_code=400, detail="No URLs provided")

    url = request.urls[0]
    fmt = request.output_format.value if request.output_format else "mp4"

    ytdlp_cmd = ["yt-dlp", "-f", request.quality.value if request.quality else "best", "-o", "-", url]

    ffmpeg_cmd = [
        "ffmpeg",
        "-i", "pipe:0",
        "-f", fmt,
        "pipe:1"
    ]

    try:
        ytdlp_proc = subprocess.Popen(ytdlp_cmd, stdout=subprocess.PIPE)
        ffmpeg_proc = subprocess.Popen(ffmpeg_cmd, stdin=ytdlp_proc.stdout, stdout=subprocess.PIPE)

        return StreamingResponse(ffmpeg_proc.stdout, media_type=f"video/{fmt}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {e}")

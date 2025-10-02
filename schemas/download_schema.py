from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, HttpUrl

class ModeEnum(str, Enum):
    VIDEO = "Video"
    AUDIO = "Audio"

class QualityEnum(str, Enum):
    BEST = "bestvideo+bestaudio/best"
    MEDIUM = "bestvideo[height<=1440]+bestaudio/best[height<=1440]"
    ABOVE_HIGH = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
    HIGH = "bestvideo[height<=720]+bestaudio/best[height<=720]"
    LOW = "bestvideo[height<=480]+bestaudio/best[height<=480]"

class FormatEnum(str, Enum):
    MKV = "Mkv"
    MP4 = "Mp4"
    MP3 = "mp3"

class DownloadRequest(BaseModel):
    urls: List[HttpUrl]
    mode: ModeEnum
    quality: Optional[QualityEnum] = None
    output_format: Optional[FormatEnum] = None
    playlist: Optional[bool] = False

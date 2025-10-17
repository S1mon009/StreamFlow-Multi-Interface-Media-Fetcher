"""
This module defines available output options for video and audio downloads,
including supported qualities and formats.
"""
OUTPUT_OPTIONS: dict[str, dict[str, list[str]]] = {
    "video": {
        "qualities": ["The best","1440p","1080p", "720p", ">=480p"],
        "formats": ["mp4", "mkv", "avi"]
    },
    "audio": {
        "formats": ["mp3", "aac", "wav"]
    }
}

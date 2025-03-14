"""
Module providing a decorator for verifying the presence of FFmpeg.

This module defines the `ffmpeg_required` decorator, which ensures that FFmpeg 
is installed before executing the decorated function.
"""

import subprocess

def ffmpeg_required(func):
    """Decorator checking that ffmpeg is installed."""
    def wrapper(*args, **kwargs):
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, check=True)
        except FileNotFoundError:
            print("Error: FFmpeg is not installed. Please install FFmpeg and try again.")
            return None
        return func(*args, **kwargs)
    return wrapper

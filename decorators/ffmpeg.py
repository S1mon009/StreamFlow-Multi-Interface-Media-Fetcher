import subprocess

def ffmpeg_required(func):
    """Decorator checking that ffmpeg is installed."""
    def wrapper(*args, **kwargs):
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, check=True)
        except Exception:
            print("Error: FFMPEG is not installed. Install FFMPEG and try again.")
            return
        return func(*args, **kwargs)
    return wrapper

"""
Video Downloader Module

This module provides a VideoDownloader class that allows users to download videos, audio,
and playlists from YouTube using yt_dlp. It supports multiple quality options, output formats,
and includes network connection handling. It also allows downloading from a .txt file
containing multiple links.
"""

import os
import time
import shutil
import subprocess
from yt_dlp import YoutubeDL
import inquirer
from dotenv import load_dotenv
from decorators.timed import timed
from decorators.ffmpeg import ffmpeg_required
from decorators.connected import is_connected, network_required


class VideoDownloader:
    """
    A class to handle video/audio downloading.

    Features:
    - Allows downloading single videos, audio, playlists, or multiple links from file.
    - Provides various quality options for video.
    - Supports multiple output formats.
    - Handles network disconnections gracefully.
    - Ensures the download folder is correctly set.
    """

    QUALITY_MAP = {
        'The best': 'bestvideo+bestaudio/best',
        'Medium (1440p)': 'bestvideo[height<=1440]+bestaudio/best[height<=1440]',
        'Above High (1080p)': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        'High (720p)': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        'Low (<=480p)': 'bestvideo[height<=480]+bestaudio/best[height<=480]'
    }
    OUTPUT_FORMATS = ['Mkv', 'Mp4']

    def __init__(self):
        load_dotenv()
        self.download_folder = os.getenv('DOWNLOAD_FOLDER',
                                         os.path.join(os.path.expanduser("~"), "Downloads"))
        self.verify_download_folder()

        self.urls = []
        self.quality = None
        self.output_format = None
        self.is_playlist = False
        self.playlist_folder = None
        self.mode = None

    def verify_download_folder(self):
        """It checks if the default download path is correct,
        and if not - it allows you to change."""
        question = [
            inquirer.Confirm('use_default',
                             message=f"Is the default download path ({self.download_folder}) correct?",
                             default=True)
        ]
        answer = inquirer.prompt(question)
        if not answer.get('use_default'):
            new_folder = inquirer.prompt([
                inquirer.Text('folder', message="Enter a new download path")
            ])
            self.download_folder = new_folder.get('folder')
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)

    def prompt_user_options(self):
        """Collect user options: source of links, mode, quality/format, playlist folder."""
        source_ans = inquirer.prompt([
            inquirer.List('source',
                          message="Choose source of links",
                          choices=['Single URL', 'TXT File'])
        ])
        source = source_ans.get('source')

        if source == 'Single URL':
            url_answer = inquirer.prompt([
                inquirer.Text('url', message="Enter the video link")
            ])
            self.urls = [url_answer.get('url')]

            if 'list=' in self.urls[0]:
                self.is_playlist = True
                folder_ans = inquirer.prompt([
                    inquirer.Text('playlist_folder', message="Enter the name of the playlist folder")
                ])
                self.playlist_folder = os.path.join(self.download_folder, folder_ans.get('playlist_folder'))
                if not os.path.exists(self.playlist_folder):
                    os.makedirs(self.playlist_folder)

        else:
            file_answer = inquirer.prompt([
                inquirer.Text('file', message="Enter the path to the TXT file with links")
            ])
            filepath = file_answer.get('file')

            if not os.path.exists(filepath):
                print(f"Error: File {filepath} not found.")
                self.urls = []
            elif not os.path.isfile(filepath):
                print(f"Error: {filepath} is not a file.")
                self.urls = []
            else:
                with open(filepath, "r", encoding="utf-8") as f:
                    self.urls = [line.strip() for line in f if line.strip()]

        mode_ans = inquirer.prompt([
            inquirer.List('mode',
                          message="Choose download mode",
                          choices=['Video', 'Audio only'])
        ])
        self.mode = mode_ans.get('mode')

        if self.mode == 'Video':
            quality_ans = inquirer.prompt([
                inquirer.List('quality',
                              message="Choose quality",
                              choices=list(self.QUALITY_MAP.keys()))
            ])
            self.quality = quality_ans.get('quality')

            format_ans = inquirer.prompt([
                inquirer.List('output_format',
                              message="Choose the output format",
                              choices=self.OUTPUT_FORMATS)
            ])
            self.output_format = format_ans.get('output_format')

    def confirm_options(self):
        """Displays the summary of selected options and asks the user to confirm."""
        summary = (
            f"\nSummary of selected options:\n"
            f"-----------------------------------\n"
            f"Number of links: {len(self.urls)}\n"
            f"Mode: {self.mode}\n"
        )
        if self.mode == "Video":
            summary += (
                f"Quality: {self.quality}\n"
                f"Output format: {self.output_format}\n"
            )
        if self.is_playlist:
            summary += f"Playlist folder: {self.playlist_folder}\n"
        summary += (
            f"Download folder: {self.download_folder}\n"
            f"-----------------------------------\n"
        )
        print(summary)
        confirm = inquirer.prompt([
            inquirer.Confirm('confirm', message="Are the above options correct?", default=True)
        ])
        return confirm.get('confirm')

    def progress_hook(self, d):
        """Hook for monitoring download progress and connection."""
        if d.get('status') == 'downloading':
            if not is_connected():
                print("\nNetwork lost. Pausing download...")
                while not is_connected():
                    time.sleep(5)
                print("Connection restored. Resuming download...")

    def detect_browser(self):
        """Detect installed browser for extracting cookies."""
        for name in ('firefox', 'chrome', 'chromium', 'edge', 'brave'):
            if shutil.which(name):
                return name
        return None

    def run_yt_dlp_with_cookies(self, output_path, url):
        """Retry with browser cookies if needed."""
        browser = self.detect_browser()
        base_cmd = ['yt-dlp', '-o', output_path, url]

        if self.mode == "Video":
            base_cmd.insert(1, '-f')
            base_cmd.insert(2, self.QUALITY_MAP[self.quality])
            base_cmd.extend(['--merge-output-format', self.output_format.lower()])
        else:  # Audio
            base_cmd.extend(['-f', 'bestaudio/best', '--extract-audio', '--audio-format', 'mp3'])

        if browser:
            print(f"Using cookies from '{browser}'...")
            base_cmd.insert(-1, '--cookies-from-browser')
            base_cmd.insert(-1, browser)
        else:
            print("No supported browser found for cookies.")

        try:
            subprocess.run(base_cmd, capture_output=True, text=True, check=True)
            print("\nSuccessful download with cookies retry!")
        except subprocess.CalledProcessError as e:
            print("\nFailed even with cookies. Error output:")
            print(e.stderr or e.stdout)

    @ffmpeg_required
    @network_required
    @timed
    def download_video(self):
        """Download all links in the chosen mode."""
        for url in self.urls:
            is_playlist = 'list=' in url
            if is_playlist and self.playlist_folder:
                output_path = os.path.join(self.playlist_folder, '%(title)s.%(ext)s')
            else:
                output_path = os.path.join(self.download_folder, '%(title)s.%(ext)s')

            if self.mode == "Video":
                ydl_opts = {
                    'format': self.QUALITY_MAP.get(self.quality, 'bestvideo+bestaudio/best'),
                    'merge_output_format': self.output_format.lower(),
                    'outtmpl': output_path,
                    'noplaylist': not is_playlist,
                    'quiet': False,
                    'progress_hooks': [self.progress_hook],
                    'postprocessors': [{
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': self.output_format.lower()
                    }],
                }
            else:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': output_path.replace("%(ext)s", "mp3"),
                    'noplaylist': not is_playlist,
                    'quiet': False,
                    'progress_hooks': [self.progress_hook],
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }

            try:
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                print(f"\nSuccessful download: {url}")
            except Exception as e:
                msg = str(e).lower()
                if 'verify' in msg and ('age' in msg or 'signed in' in msg):
                    print("\nVideo requires verification—retrying with cookies.")
                    self.run_yt_dlp_with_cookies(output_path, url)
                else:
                    print(f"\nDownload error for {url}: {e}")

"""
Video Downloader Module

This module provides a VideoDownloader class that allows users to download videos and playlists 
from YouTube using yt_dlp. It supports multiple quality options, output formats, 
and includes network connection handling.
"""

import os
import time
from yt_dlp import YoutubeDL
import inquirer
from dotenv import load_dotenv
from decorators.timed import timed
from decorators.ffmpeg import ffmpeg_required
from decorators.connected import is_connected, network_required


class VideoDownloader:
    """
    A class to handle video downloading from YouTube.

    Features:
    - Allows downloading single videos and playlists.
    - Provides various quality options.
    - Supports multiple output formats.
    - Handles network disconnections gracefully.
    - Ensures the download folder is correctly set.
    """

    QUALITY_MAP = {
    'The best': 'bestvideo+bestaudio/best',
    'Medium': 'bestvideo[height<=1440]+bestaudio/best[height<=1440]',
    'Above High': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
    'High': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
    'Low': 'bestvideo[height<=480]+bestaudio/best[height<=480]'
}
    OUTPUT_FORMATS = ['Mkv', 'Mp4']

    def __init__(self):
        load_dotenv()
        self.download_folder = os.getenv('DOWNLOAD_FOLDER',
                                         os.path.join(os.path.expanduser("~"), "Downloads"))
        self.verify_download_folder()
        self.url = None
        self.quality = None
        self.output_format = None
        self.is_playlist = False
        self.playlist_folder = None

    def verify_download_folder(self):
        """It checks if the default download path is correct, 
        and if not - it allows you to change."""
        question = [
            inquirer.Confirm('use_default',
                             message=f"Is the default download path ({self.download_folder}) is correct?",
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
        """It takes from the user downloads URL, quality options, output format and - 
        in the case of a playlist - an additional folder."""

        url_answer = inquirer.prompt([
            inquirer.Text('url', message="Enter the link to YouTube")
        ])
        self.url = url_answer.get('url')

        self.is_playlist = self.check_if_playlist(self.url)
        if self.is_playlist:
            folder_ans = inquirer.prompt([
                inquirer.Text('playlist_folder', message="Enter the name of the playlist folder")
            ])
            self.playlist_folder = os.path.join(self.download_folder,
                                                folder_ans.get('playlist_folder'))

            if not os.path.exists(self.playlist_folder):
                os.makedirs(self.playlist_folder)

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
            f"URL: {self.url}\n"
            f"Type: {'Playlist' if self.is_playlist else 'Single video'}\n"
        )
        if self.is_playlist:
            summary += f"Folder for a playlist: {self.playlist_folder}\n"
        summary += (
            f"Quality: {self.quality}\n"
            f"Output format: {self.output_format}\n"
            f"Download folder: {self.download_folder}\n"
            f"-----------------------------------\n"
        )
        print(summary)
        confirm = inquirer.prompt([
            inquirer.Confirm('confirm', message="Are the above options correct?", default=True)
        ])
        return confirm.get('confirm')

    def check_if_playlist(self, url):
        """
        Checks that the given link concerns a playlist.
        We recognize that if there is a 'list =' parameter in URL, it is a playlist.
        """
        return 'list=' in url

    def progress_hook(self, d):
        """
        Function caused periodically by YT-DLP.
        If the connection is lost - it suspends the action until the connection is restored.
        """
        if d.get('status') == 'downloading':
            if not is_connected():
                print("\nThe connection to the network was lost when downloading. Suspension of download...")
                while not is_connected():
                    time.sleep(5)
                print("Connection restored. Resumption of download...")

    @ffmpeg_required
    @network_required
    @timed
    def download_video(self):
        """Configures the YT-DLP options and performs download."""
        if self.is_playlist:
            output_path = os.path.join(self.playlist_folder, '%(title)s.%(ext)s')
        else:
            output_path = os.path.join(self.download_folder, '%(title)s.%(ext)s')

        ydl_opts = {
            'format': self.QUALITY_MAP[self.quality],
            'merge_output_format': self.output_format.lower(),
            'outtmpl': output_path,
            'noplaylist': not self.is_playlist,
            'quiet': False,
            'progress_hooks': [self.progress_hook],
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': self.output_format.lower()
            }]
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            print("\nSuccessful download.")
        except FileNotFoundError:
            print("\nError: Specified download folder does not exist.")
        except PermissionError:
            print("\nError: Insufficient permissions to save the file.")
        except KeyboardInterrupt:
            print("\nDownload interrupted by user.")

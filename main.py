"""
Main script for the Video Downloader application.

This script initializes the `VideoDownloader` class, prompts the user for download options,
and handles multiple download requests in a loop. It supports both single links and TXT files
with multiple links, as well as video or audio download modes.
"""

import time
import inquirer
from classes.video_downloader import VideoDownloader
from utils.console import clear_console


def main():
    """
    Main function that runs the video downloader application.

    Steps:
    1. Clears the console.
    2. Repeatedly prompts the user for download options (link or TXT file).
    3. If the user confirms, the download process starts.
    4. After each batch, the user is asked if they want to download more.
    5. The loop continues until the user declines further downloads.
    """

    clear_console()
    while True:
        downloader = VideoDownloader()
        downloader.prompt_user_options()

        if not downloader.urls:
            print("No valid links provided. Returning to configuration...\n")
            time.sleep(1)
            clear_console()
            continue

        if not downloader.confirm_options():
            print("Return to configuration...\n")
            time.sleep(1)
            clear_console()
            continue

        downloader.download_video()

        again = inquirer.prompt([
            inquirer.Confirm('again', message="Do you want to download more?", default=False)
        ])
        if not again.get('again'):
            print("Thank you for using the program.")
            break

        clear_console()


if __name__ == "__main__":
    main()

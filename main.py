import os
import subprocess
from yt_dlp import YoutubeDL
import inquirer

options = [
    inquirer.List('quality',
                  message="Choose quality",
                  choices=['The best', 'Medium', 'High', 'Low']),
    inquirer.List('output_format',
                  message="Choose output format",
                  choices=['Mkv', 'Mp4'])
]

quality_list = {
    'The best': 'bestvideo+bestaudio/best',
    'Medium': 'bestvideo[height<=1440]+bestaudio/best[height<=1440]',
    'High': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
    'Low': 'bestvideo[height<=480]+bestaudio/best[height<=480]'
}

DOWNLOAD_FOLDER = 'E:/Wideo'

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def check_is_playlist(url):
    """
    Prosta funkcja sprawdzająca, czy link zawiera parametr list=, 
    co zazwyczaj wskazuje, że jest to playlista.
    """
    return 'list=' in url

def download_video(url, options):
    is_playlist = check_is_playlist(url)
    
    # Jeśli link dotyczy playlisty, zapytaj o nazwę folderu i utwórz go
    if is_playlist:
        playlist_folder_name = input("Enter the name of the playlist folder: ")
        playlist_folder_path = os.path.join(DOWNLOAD_FOLDER, playlist_folder_name)
        if not os.path.exists(playlist_folder_path):
            os.makedirs(playlist_folder_path)
        output_path = os.path.join(playlist_folder_path, '%(title)s.%(ext)s')
    else:
        output_path = os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s')
    
    download_options = {
        'format': quality_list[options['quality']],
        'merge_output_format': options['output_format'].lower(),
        'outtmpl': output_path,
        # Jeśli nie jest playlistą, ustaw noplaylist na True
        'noplaylist': not is_playlist,
        'quiet': False,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': options['output_format'].lower()
        }]
    }
    
    with YoutubeDL(download_options) as ydl:
        ydl.download([url])
    print('Download completed')

if __name__ == "__main__":
    clear_console()
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, check=True) 
        if result.returncode == 0:
            # Upewnij się, że domyślny folder do pobierania istnieje
            if not os.path.exists(DOWNLOAD_FOLDER):
                os.makedirs(DOWNLOAD_FOLDER)
            url = input("Enter the url from YouTube: ")
            selected_options = inquirer.prompt(options)
            download_video(url, selected_options)
        else:
            print('ffmpeg is not installed')
    except FileNotFoundError:
        print('ffmpeg is not installed')

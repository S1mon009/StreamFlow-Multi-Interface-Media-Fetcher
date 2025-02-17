import os
import time
import socket
import subprocess
from yt_dlp import YoutubeDL
import inquirer
from dotenv import load_dotenv
from decorators.timed import timed
from decorators.ffmpeg import ffmpeg_required
from decorators.connected import is_connected, network_required
from utils.console import clear_console


class VideoDownloader:
    QUALITY_MAP = {
    'The best': 'bestvideo+bestaudio/best',
    'Medium': 'bestvideo[height<=1440]+bestaudio/best[height<=1440]',
    'Above High': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
    'High': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
    'Low': 'bestvideo[height<=480]+bestaudio/best[height<=480]'
}
    OUTPUT_FORMATS = ['Mkv', 'Mp4']

    def __init__(self):
        load_dotenv()  # Wczytuje zmienne z pliku .env
        # Jeśli zmienna DOWNLOAD_FOLDER nie istnieje, użyj domyślnej lokalizacji (np. katalogu "Downloads" użytkownika)
        self.download_folder = os.getenv('DOWNLOAD_FOLDER', os.path.join(os.path.expanduser("~"), "Downloads"))
        self.verify_download_folder()
        self.url = None
        self.quality = None
        self.output_format = None
        self.is_playlist = False
        self.playlist_folder = None

    def verify_download_folder(self):
        """Sprawdza czy domyślna ścieżka pobierania jest poprawna, a jeśli nie – umożliwia zmianę."""
        question = [
            inquirer.Confirm('use_default',
                             message=f"Czy domyślna ścieżka pobierania ({self.download_folder}) jest poprawna?",
                             default=True)
        ]
        answer = inquirer.prompt(question)
        if not answer.get('use_default'):
            new_folder = inquirer.prompt([
                inquirer.Text('folder', message="Podaj nową ścieżkę pobierania")
            ])
            self.download_folder = new_folder.get('folder')
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)

    def prompt_user_options(self):
        """Pobiera od użytkownika adres URL, opcje jakości, format wyjściowy oraz – w przypadku playlisty – dodatkowy folder."""
        # Pobranie URL
        url_answer = inquirer.prompt([
            inquirer.Text('url', message="Podaj link do YouTube")
        ])
        self.url = url_answer.get('url')

        # Sprawdzenie, czy link dotyczy playlisty
        self.is_playlist = self.check_if_playlist(self.url)
        if self.is_playlist:
            folder_ans = inquirer.prompt([
                inquirer.Text('playlist_folder', message="Podaj nazwę folderu dla playlisty")
            ])
            self.playlist_folder = os.path.join(self.download_folder, folder_ans.get('playlist_folder'))
            if not os.path.exists(self.playlist_folder):
                os.makedirs(self.playlist_folder)

        # Wybór jakości
        quality_ans = inquirer.prompt([
            inquirer.List('quality',
                          message="Wybierz jakość",
                          choices=list(self.QUALITY_MAP.keys()))
        ])
        self.quality = quality_ans.get('quality')

        # Wybór formatu wyjściowego
        format_ans = inquirer.prompt([
            inquirer.List('output_format',
                          message="Wybierz format wyjściowy",
                          choices=self.OUTPUT_FORMATS)
        ])
        self.output_format = format_ans.get('output_format')

    def confirm_options(self):
        """Wyświetla podsumowanie wybranych opcji i pyta użytkownika o potwierdzenie."""
        summary = (
            f"\nPodsumowanie wybranych opcji:\n"
            f"-----------------------------------\n"
            f"URL: {self.url}\n"
            f"Typ: {'Playlista' if self.is_playlist else 'Pojedyncze wideo'}\n"
        )
        if self.is_playlist:
            summary += f"Folder dla playlisty: {self.playlist_folder}\n"
        summary += (
            f"Jakość: {self.quality}\n"
            f"Format wyjściowy: {self.output_format}\n"
            f"Folder pobierania: {self.download_folder}\n"
            f"-----------------------------------\n"
        )
        print(summary)
        confirm = inquirer.prompt([
            inquirer.Confirm('confirm', message="Czy powyższe opcje są poprawne?", default=True)
        ])
        return confirm.get('confirm')

    def check_if_playlist(self, url):
        """
        Sprawdza, czy podany link dotyczy playlisty.
        Uznajemy, że jeśli w URL znajduje się parametr 'list=', to jest to playlista.
        """
        return 'list=' in url

    def progress_hook(self, d):
        """
        Funkcja wywoływana okresowo przez yt-dlp.
        W przypadku wykrycia utraty połączenia – wstrzymuje działanie, aż do przywrócenia połączenia.
        """
        if d.get('status') == 'downloading':
            if not is_connected():
                print("\nUtracono połączenie z siecią podczas pobierania. Wstrzymywanie pobierania...")
                while not is_connected():
                    time.sleep(5)
                print("Połączenie przywrócone. Wznawianie pobierania...")

    @ffmpeg_required
    @network_required
    @timed
    def download_video(self):
        """Konfiguruje opcje yt-dlp i wykonuje pobieranie."""
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
            print("\nPobieranie zakończone pomyślnie.")
        except Exception as e:
            print(f"\nWystąpił błąd podczas pobierania: {e}")

# ------------------------- Główna Pętla Programu -------------------------

def main():
    clear_console()
    while True:
        downloader = VideoDownloader()
        downloader.prompt_user_options()
        if not downloader.confirm_options():
            print("Powrót do konfiguracji...\n")
            time.sleep(1)
            clear_console()
            continue
        downloader.download_video()
        again = inquirer.prompt([
            inquirer.Confirm('again', message="Czy chcesz pobrać coś jeszcze?", default=False)
        ])
        if not again.get('again'):
            print("Dziękujemy za skorzystanie z programu.")
            break
        clear_console()

if __name__ == "__main__":
    main()

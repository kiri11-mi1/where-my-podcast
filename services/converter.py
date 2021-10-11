import logging
from pathlib import Path

import os
from os.path import isfile, join

import youtube_dl
from youtube_dl.utils import DownloadError


class Converter:
    def __init__(self, directory='media'):
        self.directory = directory
        Path(self.directory).mkdir(exist_ok=True)
        self.ydl_opts = {
            'outtmpl': f'{self.directory}/%(id)s.%(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '70',
            }],
        }

    def get_metadata(self, url):
        try:
            with  youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                result = ydl.extract_info(url, download=False)
                if 'entries' in result:
                    result = result['entries'][0]
                return {
                    'id': result['id'],
                    'title': result['title'],
                    'duration': result['duration']
                }
        except DownloadError:
            logging.error("URL is NOT VALID")
            return '❌ Неверный URL'

    def download(self, url):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([url])

    def clear_folder(self):
        path = f'./{self.directory}'
        for file in os.listdir(path):
            full_path = join(path, file)
            if isfile(full_path):
                os.remove(full_path)

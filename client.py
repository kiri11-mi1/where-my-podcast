from telethon.sync import TelegramClient, events
import os
import sys


def send_media_file(path):
    api_id = os.environ.get('API_ID')
    api_hash = os.environ.get('API_HASH')
    botname = 'youtube_loader_content_bot'
    with TelegramClient('test', api_id, api_hash) as client:
        client.send_file(botname, path)
        client.disconnect()


if __name__ == '__main__':
    send_media_file(sys.argv[1])

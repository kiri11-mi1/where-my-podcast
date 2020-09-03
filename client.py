from telethon.sync import TelegramClient, events
import os
import sys


def send_media_file(path):
    api_id = os.environ.get('API_ID')
    api_hash = os.environ.get('API_HASH')
    # telephone_number = os.environ.get('TELEPHONE_NUMBER')
    botname = 'youtube_loader_content_bot'
    with TelegramClient('test', api_id, api_hash) as client:
        # client.send_message(botname, 'Hello, myself!')
        client.send_file(botname, path)
        client.disconnect()


if __name__ == '__main__':
    # print(sys.argv[1])
    send_media_file(sys.argv[1])

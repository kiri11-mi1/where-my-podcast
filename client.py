from telethon.sync import TelegramClient, events
import os

def send_media_file(path):

    api_id = os.environ.get('API_ID')
    api_hash = os.environ.get('API_HASH')
    telephone_number = os.environ.get('TELEPHONE_NUMBER')
    botname = 'youtube_loader_content_bot'

    with TelegramClient('name', api_id, api_hash) as client:
        # client.send_message(botname, 'Hello, myself!')
        client.send_file(botname, path)

        client.disconnect()


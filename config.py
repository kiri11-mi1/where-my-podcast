import os

class Config:
    TOKEN = os.environ.get('API_TOKEN')
    HOST = os.environ.get('URL')
    CONTENT_TYPE = None
    CONTENT_URL = None
    CONTENT = None
    CHAT_ID = None

    # 26\ CSGO\ -\ Вертушки\ авапера.webm
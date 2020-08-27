import os

class Config:
    TOKEN = os.environ.get('API_TOKEN')
    HOST = os.environ.get('URL')
import requests


class Bot:
    '''Принимает и отправляет запросы'''

    def __init__(self, token):
        '''Добавление токена и url API'''
        self.token = token
        self.api = f'https://api.telegram.org/bot{token}/'


    def send_message(self, chat_id, text, reply_markup = None):
        '''Отправка сообщения'''
        params = {'chat_id': chat_id, 'text': text, 'reply_markup': reply_markup}
        method = 'sendMessage'
        response = requests.post(self.api + method, params).json()
        return response


    def set_webhook(self, host):
        '''Установка Webhook'''
        method='setWebhook'
        params = {'url': host}
        response = requests.get(self.api + method, params).json()
        return response


    def delete_webhook(self, host):
        '''Удаление Webhook'''
        method='deleteWebhook'
        params = {'url': host}
        response = requests.get(self.api + method, params).json()
        return response
    
    
    def send_audio(self, chat_id, audio_id):
        '''Отправка аудио'''
        method = 'sendAudio'
        params = {'chat_id': chat_id, 'audio': audio_id}
        response = requests.post(self.api + method, params).json()
        return response


    def send_video(self, chat_id, video_id):
        '''Отправка видео'''
        method = 'sendVideo'
        params = {'chat_id': chat_id, 'video': video_id}
        response = requests.post(self.api + method, params).json()
        return response

    def send_document(self, chat_id, doc_id):
        '''Отправка документа'''
        method = 'sendDocument'
        params = {'chat_id': chat_id, 'document': doc_id}
        response = requests.post(self.api + method, params).json()
        return response

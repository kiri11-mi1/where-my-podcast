import requests
import re
import pytube
import json
import os
import subprocess


class Bot:
    '''Принимает и отправляет запросы'''

    def __init__(self, token, admin_username):
        '''Инициализация глобальных переменных'''
        self.token = token
        self.api = f'https://api.telegram.org/bot{token}/'
        self.admin_username = admin_username

        self.content = None
        self.chat_id = None
        self.content_type = None
        self.content_url = None


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


    def handle(self, last_upd):
    
        keyboard = None

        if 'message' in last_upd:

            # Получение id диалога бота и пользователя
            chat_id = last_upd['message']['chat']['id']  
            
            # Если нам прислали текстовое сообщение
            if 'text' in last_upd['message']:
                user_name = last_upd['message']['chat']['first_name']
                chat_text = last_upd['message']['text']

                # Составляем текста ответа
                if chat_text in ['/help', '/start']:
                    text = f'Хочешь загрузить аудио? Тыкни ➡️ /load_audio\
                            \nХочешь загрузить видео? Тыкни ➡️ /load_video'

                elif chat_text in ['/load_audio', '/load_video']:
                    self.content_type = chat_text.replace('/load_', '')
                    if self.content_url:
                        text, keyboard = self.get_content_buttons()
                        self.content_type, self.content_url = None, None
                    else:
                        text = 'Введите URL контента с YouTube...'

                elif self.is_url(chat_text):
                    self.content_url = chat_text
                    if self.content_type:
                        text, keyboard = self.get_content_buttons()
                        self.content_type, self.content_url = None, None
                    else:
                        text = f'Хочешь загрузить аудио? Тыкни ➡️ /load_audio\
                            \nХочешь загрузить видео? Тыкни ➡️ /load_video'

                else:
                    text = f"{user_name}, я тебя не понимаю, тыкни ➡️ /help"

                # Отправка сообщения в ответ
                self.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)

            if self.is_admin(last_upd['message']['from']['username']):
                # Если отправитель админ, то мы переотправляем его медиа файл в диалог
                # с пользователем, который запросил этот файл
                if 'audio' in last_upd['message']:
                    file_id = last_upd['message']['audio']['file_id']
                    self.send_audio(self.chat_id, file_id)

                if 'video' in last_upd['message']:
                    file_id = last_upd['message']['video']['file_id']
                    self.send_video(self.chat_id, file_id)
                
                if 'document' in last_upd['message']:
                    file_id = last_upd['message']['document']['file_id']
                    self.send_document(self.chat_id, file_id)

        # Если кнопку нажали
        elif 'callback_query' in last_upd:

            # Извлекаем данные
            callback_data = last_upd['callback_query']['data']
            chat_id = last_upd['callback_query']['message']['chat']['id']

            if callback_data == 'repeat':
                # Прописать логику для повторного подключения
                pass

            else:
                if self.content:
                    text = f'👍 Загрузка прошла успешно!'
                    mime_type, _ = self.content[int(callback_data)].mime_type.split('/')
                    self.content[int(callback_data)].download('download')
                    old_filename = os.listdir('download')[0]

                    if mime_type == 'audio':
                        # Если у нас аудио -> конвертируем в mp3 -> загружаем на сервера телеграма
                        subprocess.call(['ffmpeg', 
                                         '-i',
                                         'download/'+old_filename,
                                         'download/out.mp3',
                                         '-y'])
                        os.system(f"python client.py download/out.mp3")
                    
                    elif mime_type == 'video':
                        # Если у нас видео загружаем на сервера телеграма сразу
                        subprocess.call(['python', 'client.py', 'download/'+old_filename])

                    # Присваиваем глобальной переменной текущее значение chat_id, чтобы переотправить
                    # файл с админского аккаунта, в текущий диалог
                    self.chat_id = chat_id

                    # Удаляем все файлы, чтобы не нагружать сервер
                    self.delete_all_files('download')
                    self.content = None

                else:
                    text = f'⚠️ Такого контента больше не существует, пройдите все шаги заново!'

            # Отправка сообщения в ответ
            self.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)


    def get_content_buttons(self):
        '''Возвращает выбор контента в виде кнопок'''
        buttons = []
        try:
            content = pytube.YouTube(self.content_url)

        except pytube.exceptions.RegexMatchError:
            # Возвращать текст
            return '❗️ Неверный URL', None

        except json.decoder.JSONDecodeError:
            # Возвращать текст и кнопку
            return '⚠️ Неудачное соединение, тыкните по кноке, чтобы повторить попытку',\
                    json.dumps({'inline_keyboard': [
                        { 'text': '🔃 Попробуйте ещё', 'callback_data': 'repeat' }
                        ]})
        
        if self.content_type == 'audio':
            self.content = content.streams.filter(type=self.content_type, 
                                                abr='128kbps', 
                                                mime_type="audio/mp4").all()

        elif self.content_type == 'video':
            self.content = content.streams.filter(type=self.content_type,
                                                progressive=True,
                                                res='720p').all()

        for i, val in enumerate(self.content):
            buttons.append([{ 'text': f'✅ {self.parse_name_content(str(val))}', 'callback_data': i }])
        
        return 'Выберите какого качества контент вам нужен:', json.dumps({'inline_keyboard': buttons})


    def parse_name_content(self, name):
        '''Вычленяет нужную информацию из названий файлов'''
        return ', '.join(re.findall(r"\d+fps|video/mp4|\d+p|\d+kbps|audio/\w+", name))


    def is_url(self, url):
        '''Проверка на url из YouTube'''
        template = r'https?://(?:www\.)?youtube\.com[^&\s]+(?=\s|$)'
        if re.search(template, url):
            return True
        return False


    def is_admin(self, username):
        '''Провереяет имя отправителя с именем администратора'''
        if username == self.admin_username:
            return True
        return False


    def delete_all_files(self, directory):
        '''Удаляет все файлы в папке'''
        for filename in os.listdir(directory):
            os.remove(f'{directory}/{filename}')

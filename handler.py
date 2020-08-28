import re
import pytube
import json

def is_url(url):
    template = r'https?://(?:www\.)?youtube\.com[^&\s]+(?=\s|$)'
    if re.search(template, url):
        return True
    return False

def parse_name_content(content_type, name):
        return ', '.join(re.findall(r'\d+fps|video/\w+|\d+p|\d+kbps|audio/\w+', name))

def get_content_buttons(content_type, url):
    buttons = []
    try:
        content = pytube.YouTube(url)

    except pytube.exceptions.RegexMatchError:
        # Возвращать текст
        return '❗️ Неверный URL', None

    except json.decoder.JSONDecodeError:
        # Возвращать текст и кнопку
        return '⚠️ Неудачное соединение, тыкните по кноке, чтобы повторить попытку',\
                buttons.append([{ 'text': '🔃 Попробуйте ещё', 'callback_data': 'repeat' }])
    
    for i, val in enumerate(content.streams.filter(type=content_type).all()):
        buttons.append([{ 'text': f'✅{parse_name_content(val)}', 'callback_data': i }])
    
    return buttons


def handle(last_upd, bot):
    keyboard = None
    try:
        content_url, content_type = None, None
        # Извлекаем данные для их обработки
        chat_id = last_upd['message']['chat']['id']
        chat_text = last_upd['message']['text'].lower()
        user_name = last_upd['message']['chat']['first_name']

        # Составляем текст ответов
        if chat_text == '/help':
            text = f'Хочешь загрузить аудио? Тыкни ---> /load_audio\
                     \nХочешь загрузить видео? Тыкни ---> /load_video'

        elif chat_text in ['/load_audio', '/load_video']:
            content_type = chat_text.replace('/load_', '')
            if content_url:
                # Написат функцию вывода всеx аудио или видео
                text, keyboard = 'Жмякни на кнопку с подходящими параметрами:'
            else:
                text = 'Введите URL контента с YouTube...'

        elif is_url(chat_text):
            content_url = chat_text
            if content_type:
                # Написат функцию вывода всеx аудио или видео
                text = 'Жмякни на кнопку с подходящими параметрами:'
            else:
                text = f'Хочешь загрузить аудио? Тыкни ---> /load_audio\
                       \nХочешь загрузить видео? Тыкни ---> /load_video'

        else:
            text = f"{chat_name}, я тебя не понмаю, тыкни ---> '/help'"

        # Отправка сообщения в ответ
        bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
    
    except KeyError:
            
        # Извлекаем данные
        callback_data = last_upd['callback_query']['data']
        chat_id = last_upd['callback_query']['message']['chat']['id']

        # Генерируем текст
        text = f'Принял, загрузка пошла!'

        # Отправка сообщения в ответ
        bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
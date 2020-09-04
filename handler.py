import re
import pytube
import json
import os


def write_json(data, filename='response.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def is_url(url):
    template = r'https?://(?:www\.)?youtube\.com[^&\s]+(?=\s|$)'
    if re.search(template, url):
        return True
    return False

def parse_name_content(name):
        return ', '.join(re.findall(r"\d+fps|video/\w+|\d+p|\d+kbps|audio/\w+", name))

def get_content_buttons(cfg):
    buttons = []
    try:
        content = pytube.YouTube(cfg.CONTENT_URL)

    except pytube.exceptions.RegexMatchError:
        # Возвращать текст
        return '❗️ Неверный URL', None

    except json.decoder.JSONDecodeError:
        # Возвращать текст и кнопку
        return '⚠️ Неудачное соединение, тыкните по кноке, чтобы повторить попытку',\
                json.dumps({'inline_keyboard': [
                    { 'text': '🔃 Попробуйте ещё', 'callback_data': 'repeat' }
                    ]})
    
    cfg.CONTENT = content.streams.filter(type=cfg.CONTENT_TYPE).all()

    for i, val in enumerate(cfg.CONTENT):
        buttons.append([{ 'text': f'✅ {parse_name_content(str(val))}', 'callback_data': i }])
    
    return 'Выберите какого качества контент вам нужен:', json.dumps({'inline_keyboard': buttons})


def is_admin(username):
    if username == 'kiri11_mi1':
        return True
    return False


def handle(last_upd, bot, cfg):

    keyboard = None

    if 'message' in last_upd:

        # Извлекаем данные для их обработки
        chat_id = last_upd['message']['chat']['id']  
        
        if 'text' in last_upd['message']:
            user_name = last_upd['message']['chat']['first_name']
            chat_text = last_upd['message']['text']

            # Составляем текст ответов
            if chat_text == '/help':
                text = f'Хочешь загрузить аудио? Тыкни ➡️ /load_audio\
                        \nХочешь загрузить видео? Тыкни ➡️ /load_video'

            elif chat_text in ['/load_audio', '/load_video']:
                cfg.CONTENT_TYPE = chat_text.replace('/load_', '')
                if cfg.CONTENT_URL:
                    # Написат функцию вывода всеx аудио или видео
                    text, keyboard = get_content_buttons(cfg)
                    #print(cfg.CONTENT_TYPE, cfg.CONTENT_URL)
                    cfg.CONTENT_TYPE, cfg.CONTENT_URL = None, None
                else:
                    text = 'Введите URL контента с YouTube...'

            elif is_url(chat_text):
                cfg.CONTENT_URL = chat_text
                if cfg.CONTENT_TYPE:
                    # Написат функцию вывода всеx аудио или видео
                    text, keyboard = get_content_buttons(cfg)
                    #print(cfg.CONTENT_TYPE, cfg.CONTENT_URL)
                    cfg.CONTENT_TYPE, cfg.CONTENT_URL = None, None
                else:
                    text = f'Хочешь загрузить аудио? Тыкни ➡️ /load_audio\
                        \nХочешь загрузить видео? Тыкни ➡️ /load_video'

            else:
                text = f"{user_name}, я тебя не понимаю, тыкни ➡️ /help"

            # Отправка сообщения в ответ
            bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)

        if 'audio' in last_upd['message'] and \
           is_admin(last_upd['message']['from']['username']):
            file_id = last_upd['message']['audio']['file_id']
            bot.send_audio(cfg.CHAT_ID, file_id)

        if 'video' in last_upd['message'] and \
           is_admin(last_upd['message']['from']['username']):
            file_id = last_upd['message']['video']['file_id']
            bot.send_video(cfg.CHAT_ID, file_id)
        
        if 'document' in last_upd['message'] and \
           is_admin(last_upd['message']['from']['username']):
            file_id = last_upd['message']['document']['file_id']
            bot.send_document(cfg.CHAT_ID, file_id)

    
    elif 'callback_query' in last_upd:

        # Извлекаем данные
        callback_data = last_upd['callback_query']['data']
        chat_id = last_upd['callback_query']['message']['chat']['id']

        if callback_data == 'repeat':
            # Прописать логику для повторного подключения
            pass

        else:
            if cfg.CONTENT:
                text = f'👍 Загрузка прошла успешно!'
                cfg.CONTENT[int(callback_data)].download('content')

                filename = cfg.CONTENT[int(callback_data)].title.replace(' ', '\ ')
                filename = filename.replace('#', '')
                filename = filename.replace(':', '')

                mime_type, ext = cfg.CONTENT[int(callback_data)].mime_type.split('/')

                if mime_type == 'audio':
                    os.system(f"ffmpeg -i content/{filename}.{ext} content/result.mp3 -y")
                    #print('26\ CSGO\ -\ Вертушки\ авапера.webm' == f'{filename}.{ext}')
                    os.system("python client.py content/result.mp3")
                
                elif mime_type == 'video':
                    os.system(f"python client.py content/{filename}.{ext}")

                
                cfg.CHAT_ID = chat_id
                
                # print(f'{filename}.{ext}')
                # os.system(f"rm content/{filename}.{ext}")

                cfg.CONTENT = None

            else:
                text = f'⚠️ Такого контента больше не существует, пройдите все шаги заново!'

        # Отправка сообщения в ответ
        bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)


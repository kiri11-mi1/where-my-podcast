import re
import pytube
import json
import os
import subprocess


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
    
    if cfg.CONTENT_TYPE == 'audio':
        cfg.CONTENT = content.streams.filter(type=cfg.CONTENT_TYPE, 
                                            abr='128kbps', 
                                            mime_type="audio/mp4").all()

    elif cfg.CONTENT_TYPE == 'video':
        cfg.CONTENT = content.streams.filter(type=cfg.CONTENT_TYPE,
                                            progressive=True,
                                            res='720p').all()

    for i, val in enumerate(cfg.CONTENT):
        buttons.append([{ 'text': f'✅ {parse_name_content(str(val))}', 'callback_data': i }])
    
    return 'Выберите какого качества контент вам нужен:', json.dumps({'inline_keyboard': buttons})


def delete_all_files(directory):
    for filename in os.listdir(directory):
        os.remove(f'{directory}/{filename}')


def write_json(data, filename='response.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def is_url(url):
    template = r'https?://(?:www\.)?youtube\.com[^&\s]+(?=\s|$)'
    if re.search(template, url):
        return True
    return False


def parse_name_content(name):
        return ', '.join(re.findall(r"\d+fps|video/mp4|\d+p|\d+kbps|audio/\w+", name))


def is_admin(username, cfg):
    if username == cfg.ADMIN:
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
            if chat_text in ['/help', '/start']:
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

        if is_admin(last_upd['message']['from']['username'], cfg):

            if 'audio' in last_upd['message']:
                file_id = last_upd['message']['audio']['file_id']
                bot.send_audio(cfg.CHAT_ID, file_id)

            if 'video' in last_upd['message']:
                file_id = last_upd['message']['video']['file_id']
                bot.send_video(cfg.CHAT_ID, file_id)
            
            if 'document' in last_upd['message']:
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
                cfg.CONTENT[int(callback_data)].download('download')

                mime_type, _ = cfg.CONTENT[int(callback_data)].mime_type.split('/')
                old_filename = os.listdir('download')[0]

                if mime_type == 'audio':
                    subprocess.call(['ffmpeg', '-i', 'download/'+old_filename, 'download/out.mp3', '-y'])
                    os.system(f"python client.py download/out.mp3")
                
                elif mime_type == 'video':
                    # Исправить на subprocess
                    subprocess.call(['python', 'client.py', 'download/'+old_filename])

                cfg.CHAT_ID = chat_id
                
                delete_all_files('download')

                cfg.CONTENT = None

            else:
                text = f'⚠️ Такого контента больше не существует, пройдите все шаги заново!'

        # Отправка сообщения в ответ
        bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)


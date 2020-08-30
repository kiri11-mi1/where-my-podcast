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


def handle(last_upd, bot, cfg):
    keyboard = None
    try:
        # Извлекаем данные для их обработки
        chat_id = last_upd['message']['chat']['id']
        chat_text = last_upd['message']['text']
        user_name = last_upd['message']['chat']['first_name']

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
    
    except KeyError:
            
        # Извлекаем данные
        callback_data = last_upd['callback_query']['data']
        chat_id = last_upd['callback_query']['message']['chat']['id']

        if callback_data == 'repeat':
            # Прописать логику для повторного подключения
            pass 

        else:
            if cfg.CONTENT:
                text = f'👍 Загрузка прошла успешно!'
                cfg.CONTENT[int(callback_data)].download('content/')
                filename = cfg.CONTENT[int(callback_data)].title
                ext = cfg.CONTENT[int(callback_data)].mime_type.split('/')[-1]

                # Сделать метод, который будет возвращать file_id

                write_json(bot.send_audio(chat_id, file_id))
                # os.system(f'rm ./content/\'{filename}\'.{ext}')
                cfg.CONTENT = None
            else:
                text = f'⚠️ Такого контента больше не существует, пройдите все шаги заново!'

        # Отправка сообщения в ответ
        bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
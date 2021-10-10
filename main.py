import logging

import youtube_dl
from youtube_dl.utils import DownloadError

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import NetworkError

from services.credentials import TG_TOKEN
from services.responses import START_MESSAGE, HELP_MESSAGE


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
)

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    chat_name = message.chat.username or message.chat.title
    logging.info(f'{chat_name} START messaging')
    await message.answer(START_MESSAGE)


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(HELP_MESSAGE)


@dp.message_handler()
async def parse_url(message: types.Message):
    ydl = youtube_dl.YoutubeDL({'media': '%(id)s.%(ext)s'})
    try:
        with ydl:
            result = ydl.extract_info(
                message.text,
                download=False # We just want to extract the info
            )
        if 'entries' in result:
            # Can be a playlist or a list of videos
            video = result['entries'][0]
        else:
            # Just a video
            video = result

        for f in video.get('formats'):
            if f.get('ext') == 'mp4' and f.get('asr'):
                print(f.get('url'))
                await bot.send_video(message.from_user.id, f.get('url'))
    except DownloadError:
        await message.reply('❗️ Неверный URL')


if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True)
    except NetworkError:
        logging.error('NETWORK ERROR')

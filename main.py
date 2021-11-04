import logging

from tinydb import TinyDB, Query

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import NetworkError

from services.credentials import TG_TOKEN, DATABASE
from services.responses import START_MESSAGE, HELP_MESSAGE, COMMANDS
from services.converter import Converter


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
)

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)

converter = Converter('media')
db = TinyDB(DATABASE)
Audio = Query()


@dp.message_handler(commands=['register'])
async def register(message: types.Message):
    logging.info("setting commands")
    await dp.bot.set_my_commands(COMMANDS)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    chat_name = message.chat.username or message.chat.title
    logging.info(f'{chat_name} START messaging')
    await message.answer(START_MESSAGE)


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(HELP_MESSAGE)


@dp.message_handler()
async def converting(message: types.Message):
    logging.info('SEARCHING video')
    meta = converter.get_metadata(message.text)
    if isinstance(meta, str):
        return await message.reply(meta)

    search_data = db.search(Audio.youtube_id == meta['id'])

    if search_data:
        logging.info(f"Audio {meta['title']} IS EXIST")
        return await bot.send_audio(
            message.from_user.id,
            search_data[0]['file_id'],
        )

    await message.reply('⚠️ Идёт загрузка...')
    logging.info('LOADING video')
    converter.download(message.text)

    file = open(f"{converter.directory}/{meta['id']}.mp3", "rb")
    msg = await bot.send_audio(
        message.from_user.id,
        file,
        title=meta['title'],
        performer='Audio Bot',
    )
    db.insert({'youtube_id': meta['id'], 'file_id': msg.audio.file_id})
    logging.info('video LOADED SUCCESSFULL')
    converter.clear_folder()


if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True)
    except NetworkError:
        logging.error('NETWORK ERROR')

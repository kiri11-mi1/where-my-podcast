from aiogram.types import BotCommand


COMMANDS = [
    BotCommand(command="/start", description="Давай начнём общение"),
    BotCommand(command="/help", description="Показывает список команд"),
]

START_MESSAGE = (
    "Привет!\n"
    "Я бот, который будет конвертировать в аудио видео с ютуба и вк!\n\n"
    "Хочешь разобраться, как пользоваться ботом? Тыкай /help !"
)

HELP_MESSAGE = (
    "Чтобы получить видео в аудиоформате, ты должен сбросить ссылку на видео.\n"
    "Например: https://www.youtube.com/watch?v=Dg19dcpDuzA\n"
    "Даллее бот сбросит MP3 файл."
)
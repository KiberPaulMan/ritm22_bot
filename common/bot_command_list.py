from aiogram.types import BotCommand

bot_commands = [
    BotCommand(command='start', description='Старт'),
    BotCommand(command='show_timetable', description='Просмотр расписания'),
    BotCommand(command='editing_timetable', description='Редактирование'),
    BotCommand(command='clear', description='Очистить чат'),
]

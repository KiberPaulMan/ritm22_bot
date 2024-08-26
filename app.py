import asyncio
from aiogram import Bot, Dispatcher, types
import os
from aiogram.client.default import DefaultBotProperties
from dotenv import find_dotenv, load_dotenv
from handlers.common_handlers import handlers_router
from common.bot_command_list import bot_commands
from utils.bot_schedule import scheduler

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('BOT_TOKEN'), default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()
dp.include_router(handlers_router)


async def main() -> None:
    # Run scheduler
    scheduler.start()
    # Deletes sent messages by the user when the bot is offline
    await bot.delete_webhook(drop_pending_updates=True)
    # Set command menu
    await bot.set_my_commands(commands=bot_commands, scope=types.BotCommandScopeAllPrivateChats())
    # Endless bot polling loop
    await dp.start_polling(bot)


asyncio.run(main())

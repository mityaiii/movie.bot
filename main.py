import asyncio
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from loguru import logger
from handlers import routes, command_descriptions


async def startup() -> None:
    """initialization"""
    logger.info("bot started")


async def shutdown() -> None:
    """shutdown"""
    logger.info("bot finished")


async def main():
    bot = Bot(token=os.environ.get('BOT_TOKEN'), parse_mode=ParseMode.HTML)
    await bot.set_my_commands(commands=command_descriptions)

    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(*routes)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    logger.add(
        "logs/debug.log",
        level="DEBUG",
        format="{time} | {level} | {module}:{function}:{line} | {message}",
        rotation="30 KB",
        compression="zip",
    )
    load_dotenv()

    asyncio.run(main())

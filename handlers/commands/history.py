from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from handlers.loader import film_search_engine

router = Router()


@router.message(Command("history"))
async def cmd_history(message: Message):
    search_history = await film_search_engine.get_search_history(message.from_user.id)
    search_history_answer = '\n'.join([f"{title}: {date}" for title, date in search_history])
    search_history_answer = f"""search history:
{search_history_answer}
"""
    await message.answer(search_history_answer)

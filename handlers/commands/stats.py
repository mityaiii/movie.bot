from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from handlers.loader import film_search_engine

router = Router()


@router.message(Command("stats"))
async def cmd_stats(message: Message):
    user_statistics = await film_search_engine.get_user_statistics(user_id=message.from_user.id)

    formatted_pairs = [f"{title}: {number}" for title, number in user_statistics]
    result_string = '\n'.join(formatted_pairs)
    result_string = f"""Your search statistic:
{result_string}    
"""

    await message.answer(result_string)

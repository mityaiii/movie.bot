from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from handlers.loader import film_search_engine
from core.models.success_response import SuccessResponse
from core.models.error_response import ErrorResponse

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    user_info = message.from_user

    response = await film_search_engine.add_user(
        tg_id=user_info.id,
        username=user_info.username,
        first_name=user_info.first_name,
        last_name=user_info.last_name,
    )

    if isinstance(response, SuccessResponse):
        await message.answer("Hello, you can find movie, just send title")
    elif isinstance(response, ErrorResponse):
        await message.answer("something went wrong... enter /start again")
    else:
        await message.answer(text="something went wrong...")

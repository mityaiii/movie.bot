from aiogram import Router, F
from aiogram.types import Message

from handlers.loader import film_search_engine
from core.models.error_response import ErrorResponse
from core.models.success_response import SuccessResponse

router = Router()


@router.message(F.text)
async def message_with_text(message: Message):
    message_text = message.text

    search_result = await film_search_engine.search_movie(message.from_user.id, message_text)

    if isinstance(search_result, SuccessResponse):
        movie_info = search_result.data

        text = f"""Название: {movie_info.title}
Рейтинг IMDb: {movie_info.rating}
Ссылка на IMDb: {movie_info.link}

Описание: {movie_info.description}"""

        if not movie_info.poster or movie_info.poster == 'N/A':
            await message.answer(text=text)
        else:
            await message.answer_photo(
                photo=movie_info.poster,
                caption=text
            )

    elif isinstance(search_result, ErrorResponse):
        await message.answer(text=search_result.error_message)
    else:
        await message.answer(text="something went wrong...")

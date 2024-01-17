import typing
import unicodedata

from sqlalchemy.exc import IntegrityError
from datetime import datetime

from core.models.error_response import ErrorResponse
from core.models.success_response import SuccessResponse
from core.models.response import Response
from core.entities import User, Film, SearchLog
from core.entities.kinopoisk_search_engine import KinopoiskSearchEngine
from core.entities.omdb_search_engine import OmdbSearchEngine
from core.entities.i_search_engine import ISearchEngine

from database.database import Database
from core.entities.movie_link_search_engine import MovieLinkSearchEngine


class FilmSearchEngine():
    def __init__(self) -> None:
        self.database = Database()
        self.movie_link_search_engine = MovieLinkSearchEngine()

    async def __has_russian_letters(self, text: str) -> bool:
        for char in text:
            if 'CYRILLIC' in unicodedata.name(char, ''):
                return True
        return False

    async def __create_class_based_on_letters(self, title) -> ISearchEngine:
        if await self.__has_russian_letters(title):
            return KinopoiskSearchEngine(title, self.movie_link_search_engine)
        else:
            return OmdbSearchEngine(title, self.movie_link_search_engine)

    async def search_movie(self, user_id: int, title: str) -> Response:
        search_engine: ISearchEngine = await self.__create_class_based_on_letters(title=title)

        film_response = await search_engine.find_film()

        if isinstance(film_response, ErrorResponse):
            return film_response

        film = film_response.data

        film_response = await self.add_film(
            title=film.title,
            rating=film.rating,
            poster=film.poster,
            link=film.link,
            description=film.description
        )

        if isinstance(film_response, SuccessResponse):
            response = await self.add_search_log(
                user_id=user_id,
                film_id=film_response.data.id
            )

        if isinstance(response, ErrorResponse):
            return response

        return film_response

    async def add_user(self, tg_id: int, username: str, first_name: str, last_name: str) -> Response:
        user = await self.database.get_user(tg_id=tg_id)

        if not user:
            user = User(tg_id=tg_id, username=username, first_name=first_name, last_name=last_name)

            try:
                await self.database.add_user(user=user)
            except IntegrityError as ex:
                return SuccessResponse("")
            except Exception as ex:
                return ErrorResponse(error_message=f"Error: problems with server")

        return SuccessResponse(data=user)

    async def add_search_log(self, user_id: int, film_id: int) -> Response:
        search_log = SearchLog(user_id=user_id, film_id=film_id, date=datetime.now())

        try:
            search_log = await self.database.add_search_log(search_log=search_log)
        except Exception as ex:
            return ErrorResponse(error_message=f"Error: problems with server")

        return SuccessResponse(data=search_log)

    async def add_film(self, title: str, link: str, description: str = None, rating: float = 0,
                       poster: str = None) -> Response:
        film = await self.database.get_film_by_title(title=title)

        if not film:
            film = Film(title=title, description=description, link=link, rating=rating, poster=poster)

            try:
                film = await self.database.add_film(film=film)
            except Exception as ex:
                return ErrorResponse(error_message=f"Error: problems with server")

        return SuccessResponse(data=film)

    async def get_user_statistics(self, user_id: int) -> int:
        logs = await self.database.get_user_search_logs_stats(user_id=user_id)

        return logs

    async def get_search_history(self, user_id: int) -> typing.Optional[typing.List[int]]:
        logs = await self.database.get_search_logs_by_user_id(user_id=user_id)

        return logs

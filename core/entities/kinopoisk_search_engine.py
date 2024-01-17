import typing
import aiohttp
import os

from core.entities.i_search_engine import ISearchEngine
from core.entities import Film

from core.models.error_response import ErrorResponse
from core.models.success_response import SuccessResponse

if typing.TYPE_CHECKING:
    from core.models.response import Response
    from core.entities.movie_link_search_engine import MovieLinkSearchEngine

KINOPOISK_API_KEY = os.environ.get('KINOPOISK_API_KEY')


class KinopoiskSearchEngine(ISearchEngine):
    def __init__(self, title: str, movie_link_search_engine: "MovieLinkSearchEngine") -> None:
        self.title = title
        self.movie_link_search_engine = movie_link_search_engine

    async def find_film(self) -> "Response":
        headers = {'X-API-KEY': KINOPOISK_API_KEY}

        async with aiohttp.ClientSession() as session:
            kinopoisk_url = f'https://api.kinopoisk.dev/v1.4/movie/search?query={self.title}'

            async with session.get(kinopoisk_url, headers=headers) as response:
                if response.status != 200:
                    return ErrorResponse(f"Request to Kinopoisk API failed with status code: {response.status}")

                data = await response.json()

            if 'Error' in data:
                return ErrorResponse(data.get('Error', 'N/A'))

        data = data['docs'][0]

        title = data.get('name', 'N/A')
        rating = data.get('internalRating', 'N/A')
        if rating == 'N/A':
            data['rating']['kp']
        poster_url = data.get('poster', 'N/A')
        if poster_url != 'N/A':
            poster_url = poster_url['url']
        
        genres = data.get('genres', 'N/A')
        if any(item["name"] == "аниме" for item in genres):
            link = await self.movie_link_search_engine.find_movie(title, True)
        else:
            link = await self.movie_link_search_engine.find_movie(title)
        # kp_link = f"https://www.kinopoisk.ru/film/{data.get('id', 'N/A')}/"
        description = data.get('description', 'N/A')

        film = Film(
            title=title,
            rating=rating,
            poster=poster_url,
            link=link,
            description=description,
        )

        return SuccessResponse(data=film)

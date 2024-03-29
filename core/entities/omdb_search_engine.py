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

OMDB_API_KEY = os.environ.get('OMDB_API_KEY')


class OmdbSearchEngine(ISearchEngine):
    def __init__(self, title, movie_link_search_engine: "MovieLinkSearchEngine") -> None:
        self.title = title
        self.movie_link_search_engine = movie_link_search_engine

    async def find_film(self) -> "Response":
        async with aiohttp.ClientSession() as session:
            omdb_url = f'http://www.omdbapi.com/?t={self.title}&apikey={OMDB_API_KEY}'
            async with session.get(omdb_url) as response:
                if response.status != 200:
                    return ErrorResponse(f"Request to OMDB API failed with status code: {response.status}")

                data = await response.json()

            if 'Error' in data:
                return ErrorResponse(data.get('Error', 'N/A'))

        title = data.get('Title', 'N/A')
        rating = data.get('imdbRating', 'N/A')
        poster_url = data.get('Poster', 'N/A')
        # imdb_link = f"https://www.imdb.com/title/{data.get('imdbID', 'N/A')}/"
        link = await self.movie_link_search_engine.find_movie(title)
        description = data.get('Plot', 'N/A')

        film = Film(
            title=title,
            rating=rating,
            poster=poster_url,
            link=link,
            description=description,
        )

        return SuccessResponse(data=film)

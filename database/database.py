import typing
import asyncio
import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select, func
from sqlalchemy.exc import NoResultFound

from database.models import UserModel, FilmModel, SearchLogModel
from database import Base
from core.entities import Film, User, SearchLog

DATABASE_URL = os.environ.get('DATABASE_URL')


class Database:
    def __init__(self, database_url='sqlite+aiosqlite:///example.db'):
        self.engine = None
        self.database_url = database_url
        self.Session = None

        asyncio.get_event_loop().run_until_complete(self.async_init())

    async def async_init(self):
        self.engine = create_async_engine(self.database_url)
        self.Session = async_sessionmaker(bind=self.engine)

        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def add_user(self, user: "User") -> None:
        user_model = UserModel(id=user.tg_id, username=user.username, first_name=user.first_name,
                               last_name=user.last_name)
        async with self.Session() as session:
            session.add(user_model)
            await session.commit()

    async def get_user(self, tg_id: int) -> typing.Optional["User"]:
        async with self.Session() as session:
            user_model = await session.get(UserModel, tg_id)

            if user_model:
                return User(tg_id=user_model.id, username=user_model.username, first_name=user_model.first_name,
                            last_name=user_model.last_name)
            else:
                return None

    async def add_film(self, film: "Film") -> typing.Optional["Film"]:
        film_model = FilmModel(title=film.title, description=film.description, link=film.link, rating=film.rating,
                               poster=film.poster)

        async with self.Session() as session:
            session.add(film_model)
            await session.commit()
            await session.refresh(film_model)
            new_film = Film.from_model(film_model=film_model)
            return new_film

    async def get_film_by_title(self, title: str) -> typing.Optional["Film"]:
        async with self.Session() as session:
            query = select(FilmModel).filter(FilmModel.title == title)
            result = await session.execute(query)
            film_model = result.scalar_one_or_none()

            if film_model:
                return Film.from_model(film_model=film_model)
            else:
                return None

    async def add_search_log(self, search_log: "SearchLog") -> typing.Optional["SearchLog"]:
        search_log_model = SearchLogModel(user_id=search_log.user_id, film_id=search_log.film_id, date=search_log.date)
        async with self.Session() as session:
            session.add(search_log_model)
            await session.commit()

    async def get_search_logs_by_user_id(self, user_id) -> typing.Optional[typing.List["SearchLog"]]:
        film_table = FilmModel.__table__
        search_log_table = SearchLogModel.__table__

        try:
            async with self.Session() as session:
                stmt = select(
                    film_table.c.title,
                    search_log_table.c.date,
                ) \
                    .join(search_log_table, search_log_table.c.film_id == film_table.c.id) \
                    .where(search_log_table.c.user_id == user_id)

                result = await session.execute(stmt)
                search_logs = result.fetchall()

                formatted_search_logs = [(title, date.strftime("%H:%M:%S %d-%m-%Y")) for title, date in search_logs]

                return formatted_search_logs
        except NoResultFound:
            return None

    async def get_user_search_logs_stats(self, user_id):
        async with self.Session() as session:
            film_table = FilmModel.__table__
            search_log_table = SearchLogModel.__table__

            stmt = select(
                film_table.c.title,
                func.count().label('search_count')
            ) \
                .join(search_log_table, search_log_table.c.film_id == film_table.c.id) \
                .where(search_log_table.c.user_id == user_id) \
                .group_by(film_table.c.title)

            result = await session.execute(stmt)
            search_stats = result.fetchall()

            return search_stats

    async def close(self):
        await self.engine.dispose()

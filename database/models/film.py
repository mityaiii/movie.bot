from sqlalchemy import Column, Integer, String, Text, SmallInteger

from database import Base


class FilmModel(Base):
    __tablename__ = 'Films'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(Text, nullable=True)
    link = Column(String)
    rating = Column(SmallInteger)
    poster = Column(String, nullable=True)

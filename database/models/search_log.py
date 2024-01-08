from sqlalchemy import Column, Integer, DateTime

from database import Base


class SearchLogModel(Base):
    __tablename__ = 'SearchLogs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    film_id = Column(Integer)
    date = Column(DateTime)

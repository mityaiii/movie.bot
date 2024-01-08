from sqlalchemy import Column, Integer, String

from database import Base


class UserModel(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, autoincrement=False)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String, nullable=True)

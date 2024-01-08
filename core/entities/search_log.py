from dataclasses import dataclass
from datetime import datetime


@dataclass
class SearchLog:
    user_id: int
    film_id: int
    id: int = None
    date: datetime.date = None

    @classmethod
    def from_model(cls, search_log_model):
        return cls(
            id=search_log_model.id,
            user_id=search_log_model.user_id,
            film_id=search_log_model.film_id,
            date=search_log_model.date,
        )

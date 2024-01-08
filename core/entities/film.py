from dataclasses import dataclass


@dataclass
class Film:
    title: str
    link: str
    id: int = None
    description: str = None
    rating: float = 0
    poster: str = None

    @classmethod
    def from_model(cls, film_model):
        return cls(
            id=film_model.id,
            title=film_model.title,
            link=film_model.link,
            description=film_model.description,
            rating=film_model.rating,
            poster=film_model.poster,
        )

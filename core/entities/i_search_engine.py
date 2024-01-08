import typing
from abc import ABC, abstractmethod

if typing.TYPE_CHECKING:
    from core.models.response import Response


class ISearchEngine(ABC):
    @abstractmethod
    async def find_film(self) -> "Response":
        pass

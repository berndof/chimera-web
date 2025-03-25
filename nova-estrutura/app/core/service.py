from typing import Generic, TypeVar

from app.core.repository import BaseRepository

T = TypeVar("T")

R = TypeVar("R", bound=BaseRepository[T])  # type: ignore


class BaseService(Generic[T, R]):
    def __init__(self, repository: R):
        self.repository = repository

import logging
from typing import Generic, TypeVar

from app.core.x_repository import BaseRepository

R = TypeVar("R", bound=BaseRepository[T])  # type: ignore


class BaseService(Generic[T, R]):
    def __init__(self, repository: R):
        self.logger = logging.getLogger(f"{T.__name__} Service")
        self.repository = repository

from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ListResponse(BaseModel, Generic[T]):
    total: int
    page: int
    per_page: int
    total_pages: int
    items: list[T]

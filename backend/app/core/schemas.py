from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str
    # user id?


class UserLogin(BaseModel):
    username: str
    password: str


class HealthResponse(BaseModel):
    status: str
    message: str | None = None


class ListResponse(BaseModel, Generic[T]):
    total: int
    page: int
    per_page: int
    total_pages: int
    items: list[T]

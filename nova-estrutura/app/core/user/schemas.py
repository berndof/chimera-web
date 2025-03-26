import uuid
from datetime import datetime
from typing import Annotated

from pydantic import EmailStr, Field, StringConstraints

from app.core.pagination.schemas import StringFilterField
from app.core.types import BaseFilter, BaseSchema

from .models import User


class UserBase(BaseSchema[User]):
    username: Annotated[
        str, StringConstraints(min_length=3, max_length=30, pattern=r"^\w+$")
    ] = Field(..., example="john_doe")

    email: EmailStr | None = Field(None, example="john.doe@example.com")

    first_name: Annotated[
        str, StringConstraints(min_length=2, max_length=50, pattern=r"^[A-Za-z]+$")
    ] = Field(..., example="John")

    last_name: Annotated[
        str, StringConstraints(min_length=2, max_length=50, pattern=r"^[A-Za-z]+$")
    ] = Field(..., example="Doe")

    @classmethod
    def validate_first_name(cls, first_name: str) -> str:
        return first_name.capitalize()

    @classmethod
    def validate_last_name(cls, last_name: str) -> str:
        return last_name.capitalize()


class UserPublic(UserBase): ...


class UserIn(UserBase):
    password: Annotated[str, StringConstraints(min_length=8)]


class UserDetail(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class UserFilter(BaseFilter[UserBase]):
    username: StringFilterField | None = None
    email: StringFilterField | None = None
    first_name: StringFilterField | None = None
    last_name: StringFilterField | None = None

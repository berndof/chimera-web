from typing import Annotated

from pydantic import Field, StringConstraints

from app.core.pagination.schemas import StringFilterField
from app.core.types import BaseFilter, BaseSchema

from .models import Role


class RoleBase(BaseSchema[Role]):
    name: Annotated[
        str, StringConstraints(min_length=3, max_length=30, pattern=r"^[a-z_]+$")
    ] = Field(..., example="default_users")
    detail: Annotated[
        str | None,
        StringConstraints(min_length=3, max_length=30, pattern=r"^[A-Za-z_]+$"),
    ] = Field(None, example="notes...")


class RoleFilter(BaseFilter[RoleBase]):
    name: StringFilterField | None = None


class RoleIn(RoleBase): ...

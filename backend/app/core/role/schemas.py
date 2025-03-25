from uuid import UUID

from pydantic import BaseModel, ConfigDict
from app.core.user.schemas import UserResponse
from datetime import datetime


class RoleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    description: str | None = None


class RoleCreate(RoleBase):
    pass


class RoleResponse(RoleBase):
    id: UUID


class RoleDetail(RoleBase):
    id: UUID
    users: list[UserResponse] = []
    created_at: datetime
    updated_at: datetime


class RoleUserAdd(BaseModel):
    role_name: str
    username: str

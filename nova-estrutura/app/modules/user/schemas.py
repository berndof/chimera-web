import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    email: str
    first_name: str
    last_name: str


class UserIn(UserBase):
    password: str


class UserDetail(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

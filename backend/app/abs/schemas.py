from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

from app.database.dependencies import Base

T = TypeVar("T", bound="Base")

class BaseSchema(BaseModel, Generic[T]):
    model_config = ConfigDict(from_attributes=True)


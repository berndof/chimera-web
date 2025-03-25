from pydantic import BaseModel, ConfigDict


class ItemBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    description: str | None = None


class ItemDetail(ItemBase):
    id: int

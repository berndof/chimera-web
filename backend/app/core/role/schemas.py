from pydantic import BaseModel, ConfigDict


class RoleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    description: str | None = None


class RoleCreate(RoleBase):
    pass


class RoleResponse(RoleBase):
    pass

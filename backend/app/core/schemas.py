from pydantic import BaseModel


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

from app.core.user.exceptions import UserAlreadyExists
from app.core.user.model import User
from app.core.user.repository import UserRepository
from app.core.user.schemas import UserCreate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create(self, user_in: UserCreate) -> User:
        exists = await self.repository.get_by_username(user_in.username)
        if exists:
            raise UserAlreadyExists()
        new_user = await self.repository.create(user_in)
        return new_user

    async def get_by_username(self, username: str) -> User | None:
        return await self.repository.get_by_username(username)

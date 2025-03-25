import logging

from app.core.user.exceptions import UserAlreadyExists, UserNotExists
from app.core.user.model import User
from app.core.user.repository import UserRepository
from app.core.user.schemas import UserCreate


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository: UserRepository = repository
        self.logger = logging.getLogger("USER_SERVICE")
        self.logger.setLevel(logging.DEBUG)

    async def create(self, user_in: UserCreate) -> User:
        user_exists: User | None = await self.repository.get_by_username(
            user_in.username
        )

        if user_exists:
            raise UserAlreadyExists()
        new_user: User = await self.repository.create(user_in)
        return new_user

    async def get_by_username(self, username: str) -> User:
        user = await self.repository.get_by_username(username)
        if user is None:
            raise UserNotExists()
        return user

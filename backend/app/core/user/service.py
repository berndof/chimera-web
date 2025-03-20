import logging

from app.core.user.exceptions import UserAlreadyExists
from app.core.user.repository import UserRepository
from app.core.user.schemas import UserCreate
from app.models import User


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository: UserRepository = repository
        self.logger = logging.getLogger("USER_SERVICE")
        self.logger.setLevel(logging.DEBUG)

    async def create(self, user_in: UserCreate) -> User:
        self.logger.debug(f"creating user, input data: {user_in}")

        user_exists: User | None = await self.repository.get_by_username(
            user_in.username
        )

        if user_exists:
            raise UserAlreadyExists()
        new_user: User = await self.repository.create(user_in)
        return new_user

    async def get_by_username(self, username: str) -> User | None:
        return await self.repository.get_by_username(username)

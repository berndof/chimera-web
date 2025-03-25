from app.core.service import BaseService

from .models import User
from .repository import UserRepository
from .schemas import UserIn


class UserService(BaseService[User, UserRepository]):
    async def create(self, user_in: UserIn) -> User:
        new_user: User = await self.repository.create(user_in)
        return new_user

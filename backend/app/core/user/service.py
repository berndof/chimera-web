from app.core.types import BaseSchema, BaseService

from .models import User
from .repository import UserRepository
from .schemas import UserFilter, UserIn


class UserService(BaseService[User, UserRepository]):
    async def create(self, user_in: UserIn) -> User:
        # add user to default role
        return await self.repository.create(user_in)

    async def get_by_username(self, username: str) -> User:
        return await self.repository.get_by_username(username)

    async def get_by_id(self, id: str) -> User:
        return await self.repository.get_by_id(id)

    async def get_list(
        self,
        response_schema: BaseSchema[User],
        page: int,
        per_page: int,
        sort_by: str,
        order: str,
        filters: UserFilter,
    ):
        return await self.repository.get_list(
            response_schema, page, per_page, sort_by, order, filters
        )

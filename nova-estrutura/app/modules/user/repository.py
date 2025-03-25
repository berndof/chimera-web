from sqlalchemy.future import select

from app.core.repository import BaseRepository
from app.core.security import get_password_hash

from .models import User
from .schemas import UserIn


class UserRepository(BaseRepository[User]):
    async def create(self, user_in: UserIn) -> User:
        # log
        try:
            new_user = User(
                username=user_in.username,
                email=user_in.email,
                password=get_password_hash(user_in.password),
                first_name=user_in.first_name,
                last_name=user_in.last_name,
            )

            await self.save(new_user)
            return new_user
        except Exception as e:
            raise e

    async def get_by_username(self, username: str) -> User:
        # log
        stmt = select(self.model).where(self.model.username == username)
        try:
            result = await self.db_session.execute(stmt)
            user = result.scalar_one()
        except Exception as e:
            raise e
        return user

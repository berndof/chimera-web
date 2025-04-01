from sqlalchemy.exc import IntegrityError

from app.core.user.models import User
from app.core.user.schemas import UserIn
from app.database.exceptions import DuplicateEntryError
from app.types.repository import BaseRepository
from app.utils.security import get_password_hash


class UserRepository(BaseRepository[User]):
    async def create(self, user_in: UserIn) -> User:
        self.logger.debug(f"Creating user with data: {user_in.model_dump_json()}")
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
        except IntegrityError as ie:
            if "ix_user_username" in str(ie.orig):
                raise DuplicateEntryError(User)
            raise ie

    """ async def get_by_username(self, username: str) -> User:
        stmt = select(self.model).where(self.model.username == username)
        self.logger.debug(f"Searching user with {stmt}")
        try:
            result = await self.db_session.execute(stmt)
            user = result.scalar_one()
            return user
        except Exception as e:
            self.logger.error(e)
            raise e

    async def get_by_id(self, id: str) -> User:
        stmt = select(self.model).where(self.model.id == id)
        self.logger.debug(f"Searching user with {stmt}")
        try:
            result = await self.db_session.execute(stmt)
            user = result.scalar_one()
            return user
        except Exception as e:
            self.logger.error(e)
            raise e """

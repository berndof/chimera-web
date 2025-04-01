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

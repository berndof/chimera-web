from fastapi import HTTPException, status

from app.core.user.models import User
from app.core.user.repository import UserRepository
from app.core.user.schemas import UserIn
from app.database.exceptions import DuplicateEntryError
from app.types.service import BaseService


class UserService(BaseService[UserRepository]):
    async def create(self, user_in: UserIn) -> User:
        try:
            new_user = await self.repository.create(user_in)
            return new_user
        except DuplicateEntryError as dee:
            self.logger.debug(f"Usuário duplicado: {dee}")
            # Levanta uma exceção HTTP 409 (Conflict)
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(dee))
        except Exception as e:
            self.logger.error(e)
            # Para outros erros, você pode levantar uma exceção genérica ou customizada
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno no servidor. {e}",
            )

from fastapi import HTTPException, status

from app.core.types import BaseService
from app.database.exceptions import DuplicateEntryError

from app.core.user.models import User
from app.core.user.repository import UserRepository
from app.core.user.schemas import UserIn


class UserService(BaseService[User, UserRepository]):
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


"""     async def get_list(
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
        ) """

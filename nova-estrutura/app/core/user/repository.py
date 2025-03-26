from sqlalchemy.future import select

from app.core.security import get_password_hash
from app.core.types import BaseRepository

from .models import User
from .schemas import UserIn


class UserRepository(BaseRepository[User]):
    async def create(self, user_in: UserIn) -> User:
        self.logger.debug(f"Creating user with data: {UserIn}")
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
            self.logger.error(e)
            raise e

    async def get_by_username(self, username: str) -> User:
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
            raise e


"""     async def get_list(
        self,
        page: int,
        per_page: int,
        sort_by: str,
        order: str,
        filters: UserFilter | None = None,
    ) -> PaginatedResponse[UserBase]:
        self.logger.debug(
            f"Fetching {per_page} Users sorted by {sort_by}, order {order}, page {page}, "
            f"filters: {filters.model_dump() if filters else {}}"
        )
        offset = (page - 1) * per_page
        self.logger.debug(f"Calculated offset: {offset}")

        # Inicializa a query de contagem e a query de busca
        count_query = select(func.count()).select_from(self.model)
        query = select(self.model)
        self.logger.debug(f"Initial count query: {count_query}")
        self.logger.debug(f"Initial query: {query}")

        # Aplica os filtros se houver
        if filters:
            filter_dict = filters.model_dump(exclude_unset=True)
            self.logger.debug(f"Filters applied: {filter_dict}")
            if filter_dict:
                conditions = [
                    getattr(self.model, key) == value
                    for key, value in filter_dict.items()
                ]
                query = query.where(and_(*conditions))
                count_query = count_query.where(and_(*conditions))
                self.logger.debug(f"Updated count query with filters: {count_query}")
                self.logger.debug(f"Updated query with filters: {query}")

        if filters:
            filter_dict = filters.model_dump(exclude_unset=True, exclude_none=True)
            if filter_dict:
                conditions = []
                for key, value in filter_dict.items():
                    column = getattr(self.model, key)
                    # Se o valor for string, usa ilike para busca parcial
                    if isinstance(value, str):
                        conditions.append(column.ilike(f"%{value}%"))
                    else:
                        conditions.append(column == value)
                query = query.where(and_(*conditions))
                count_query = count_query.where(and_(*conditions))

        # Executa a contagem total
        total_results = await self.db_session.execute(count_query)
        total = total_results.scalar_one()
        self.logger.debug(f"Total results count: {total}")

        total_pages = (total + per_page - 1) // per_page if total > 0 else 1
        self.logger.debug(f"Total pages calculated: {total_pages}")

        # Se a página solicitada for maior que o total, retorna itens vazios
        if page > total_pages:
            self.logger.debug(
                f"Requested page {page} exceeds total pages {total_pages}"
            )
            return PaginatedResponse(
                total=total,
                page=page,
                per_page=per_page,
                total_pages=total_pages,
                items=None,
            )

        # Ordenamento
        sort_column = getattr(self.model, sort_by)
        order_func = asc if order == "asc" else desc
        self.logger.debug(f"Sorting by column: {sort_column}, order: {order}")

        query = query.order_by(order_func(sort_column)).offset(offset).limit(per_page)
        self.logger.debug(f"Final query with sorting and pagination: {query}")

        result = await self.db_session.execute(query)o
        items = [UserBase.model_validate(item) for item in result.scalars().all()]
        self.logger.debug(f"Fetched items: {items}")

        self.logger.debug(f"Validated items: {items}")

        return PaginatedResponse[UserBase](
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
            items=items,
        )
 """

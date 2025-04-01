import logging
from typing import Any, Generic, Sequence, TypeVar

from sqlalchemy import asc, desc, func, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import Base
from app.types.schemas import BaseSchema
from app.utils.pagination.dependencies import apply_filters
from app.utils.pagination.schemas import BaseFilter

T = TypeVar("T", bound="Base")
S = TypeVar("S", bound="BaseSchema")

class BaseRepository(Generic[T]):
    """
    Repositório genérico que opera sobre um modelo SQLAlchemy.
    """
    def __init__(self, db_session: AsyncSession, model: type[T]) -> None:
        self.db_session = db_session
        self.model = model
        self.logger = logging.getLogger(f"{model.__name__} Repository")

    async def save(self, obj: T) -> None:
        self.db_session.add(obj)
        await self.db_session.flush()
        await self.db_session.refresh(obj)

    async def get_list(
        self,
        page: int,
        per_page: int,
        sort_by: str,
        order: str,
        filters: BaseFilter[S],
    ) -> tuple[int, int, int, int, Sequence[T]]:
        offset = (page - 1) * per_page
        self.logger.debug(f"Offset = {offset}")

        # Query de contagem
        count_query = select(func.count()).select_from(self.model)
        query = select(self.model)

        # Se houver filtros (usando model_dump para Pydantic v2; em v1 use .dict())
        filter_dict = filters.model_dump(exclude_unset=True, exclude_none=True)
        if filter_dict:
            query = apply_filters(query, self.model, filters=filter_dict)
            count_query = apply_filters(count_query, self.model, filters=filter_dict)

        total_results = await self.db_session.execute(count_query)
        total = total_results.scalar_one()
        self.logger.debug(f"Total results = {total}")

        total_pages = (total + per_page - 1) // per_page if total > 0 else 1
        self.logger.debug(f"Total pages = {total_pages}")
        if page <= total_pages:
            # Ordenação
            if hasattr(self.model, sort_by):
                sort_column = getattr(self.model, sort_by)
                order_func = asc if order.lower() == "asc" else desc
                query = query.order_by(order_func(sort_column))
                self.logger.debug(f"Sort by {sort_by} {order}")
            else:
                self.logger.debug("Sort field does not exist")

            query = query.offset(offset).limit(per_page)
            result = await self.db_session.execute(query)
            items = result.scalars().all()
            
            self.logger.debug(f"Results = {items}")
            
            return total, page, per_page, total_pages, items
        else: 
            raise NoResultFound()

            

        return total, page, per_page, total_pages, items

    async def get_by(self, field: str, value: Any) -> T:
        if not hasattr(self.model, field):
            self.logger.error(
                f"Field '{field}' does not exist in {self.model.__name__}"
            )
            raise ValueError(f"Field '{field}' does not exist in {self.model.__name__}")

        query = select(self.model).where(getattr(self.model, field) == value)

        self.logger.debug(f"Executing query: {query}")

        result = await self.db_session.execute(query)
        try:
            return result.scalar_one()
        except NoResultFound as nrf:
            self.logger.debug(f"No {self.model.__name__} found with {field} = {value}")
            raise nrf
        except Exception as e:
            raise e

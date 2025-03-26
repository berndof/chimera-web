import logging
from typing import Generic

from sqlalchemy import asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .pagination.filters import apply_filters  # type: ignore
from .pagination.schemas import BaseFilter, PaginatedResponse
from .types import BASE_SCHEMA, MODEL


class BaseRepository(Generic[MODEL, BASE_SCHEMA]):
    def __init__(self, db_session: AsyncSession, model: type[MODEL]):
        self.db_session = db_session
        self.model = model
        self.logger = logging.getLogger(f"{model.__name__} Repository")

    async def save(self, obj: MODEL) -> None:
        self.db_session.add(obj)
        await self.db_session.flush()
        await self.db_session.refresh(obj)

    async def get_list(
        self,
        response_schema: BASE_SCHEMA,
        page: int,
        per_page: int,
        sort_by: str,
        order: str,
        filters: BaseFilter[MODEL],
    ) -> PaginatedResponse[BASE_SCHEMA]:
        offset = (page - 1) * per_page
        self.logger.debug(f"Offset = {offset}")

        # Query de contagem
        count_query = select(func.count()).select_from(self.model)
        query = select(self.model)

        # Filters
        filter_dict = filters.model_dump(exclude_unset=True, exclude_none=True)
        if filter_dict:
            query = apply_filters(query, self.model, filters=filter_dict)
            count_query = apply_filters(count_query, self.model, filters=filter_dict)

        total_results = await self.db_session.execute(count_query)
        total = total_results.scalar_one()
        self.logger.debug(f"Total results = {total}")

        total_pages = (total + per_page - 1) // per_page if total > 0 else 1
        self.logger.debug(f"Total pages = {total_pages}")

        if page > total_pages:
            self.logger.debug("Page is > total pages")
            return PaginatedResponse[BASE_SCHEMA](
                total=total,
                page=page,
                per_page=per_page,
                total_pages=total_pages,
                items=None,
            )

        # Ordenação
        if hasattr(self.model, sort_by):
            sort_column = getattr(self.model, sort_by)
            order_func = asc if order.lower() == "asc" else desc
            query = query.order_by(order_func(sort_column))
            self.logger.debug(f"Sort by {sort_by} {order}")
        else:
            self.logger.debug("Sort field does not exists")

        query = query.offset(offset).limit(per_page)
        self.logger.debug(f"Final query = {query}")

        result = await self.db_session.execute(query)
        items = [
            response_schema.model_validate(item) for item in result.scalars().all()
        ]
        self.logger.debug(f"Results = {items}")

        return PaginatedResponse[BASE_SCHEMA](
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
            items=items,
        )

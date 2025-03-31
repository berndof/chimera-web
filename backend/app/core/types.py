import logging
from typing import Any, Generic, TypeVar

from core.pagination.dependencies import apply_filters
from fastapi import HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import asc, desc, func, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

MODEL = TypeVar("MODEL")

BASE_SCHEMA = TypeVar("BASE_SCHEMA", bound="BaseSchema")  # type: ignore

BASE_REPOSITORY = TypeVar("BASE_REPOSITORY", bound="BaseRepository[MODEL]")  # type: ignore


class BaseSchema(BaseModel, Generic[MODEL]):
    """Schema base genérico para todos os modelos."""

    model_config = ConfigDict(from_attributes=True)


class PaginatedResponse(BaseModel, Generic[BASE_SCHEMA]):
    total: int
    page: int
    per_page: int
    total_pages: int
    items: None | list[BASE_SCHEMA]


class BaseFilter(BaseModel, Generic[BASE_SCHEMA]):
    pass


class BaseRepository(Generic[MODEL]):
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
        response_schema: type[BASE_SCHEMA],
        page: int,
        per_page: int,
        sort_by: str,
        order: str,
        filters: BaseFilter[BASE_SCHEMA],
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

    async def get_by(self, field: str, value: Any) -> MODEL:
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


class BaseService(Generic[MODEL, BASE_REPOSITORY]):
    def __init__(self, repository: BaseRepository[MODEL]):
        self.logger = logging.getLogger(f"{self.repository.model.__name__} Service")
        self.repository = repository

    async def get_list(
        self,
        response_schema: type[BASE_SCHEMA],
        page: int,
        per_page: int,
        sort_by: str,
        order: str,
        filters: BaseFilter[BASE_SCHEMA],
    ) -> PaginatedResponse[BASE_SCHEMA]:
        return await self.repository.get_list(
            response_schema, page, per_page, sort_by, order, filters # type: ignore
        )

    async def get_by(self, field: str, value: Any) -> MODEL | None:
        try:
            item = await self.repository.get_by(field, value)
            return item
        except NoResultFound:
            self.logger.debug(
                f"No {self.repository.model.__name__} found with {field} = {value}"
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.repository.model.__name__} not found",
            )
        except Exception as e:
            self.logger.error("subindo uma exceção diferente")
            raise e

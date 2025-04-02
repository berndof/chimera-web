import logging
from typing import Any, Generic, TypeVar

from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound

from app.abs.repository import BaseRepository
from app.abs.schemas import BaseSchema
from app.database.dependencies import Base
from app.utils.pagination.schemas import BaseFilter, PaginatedResponse

T = TypeVar("T", bound="BaseRepository")
U = TypeVar("U", bound="BaseSchema")
V = TypeVar("V", bound="Base")

class BaseService(Generic[T]):
    """backend
    Serviço genérico que utiliza um repositório para operações comuns.
    """
    def __init__(self, repository: T) -> None:
        self.repository = repository
        self.logger = logging.getLogger(f"{self.repository.model.__name__} Service")

    async def get_list(
        self,
        response_schema: type[U],
        page: int,
        per_page: int,
        sort_by: str,
        order: str,
        filters: BaseFilter[U],
    ) ->PaginatedResponse[U]:
        try:
            _total, _page, _per_page, _total_pages, _items  = await self.repository.get_list(
                page, per_page, sort_by, order, filters
            )

            items = [response_schema.model_validate(item) for item in _items] 
            self.logger.info(f"Fetched {len(items)} items from the database, {items}")

            return PaginatedResponse[U](
                total=_total,
                page=_page,
                per_page=_per_page,
                total_pages=_total_pages,
                items=items,
            )

        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.repository.model.__name__} not found",
            )
        except Exception as e:
            self.logger.error(f"Error fetching list: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )

    async def get_by(self, field: str, value: Any) -> V:
        try:
            return await self.repository.get_by(field, value)
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.repository.model.__name__} not found",
            )


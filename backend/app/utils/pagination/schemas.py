
from typing import Generic, TypeVar

from app.types.schemas import BaseSchema
from pydantic import BaseModel, Field

T = TypeVar("T", bound="BaseSchema")

class PaginatedResponse(BaseModel, Generic[T]):
    """
    A generic paginated response model.
    """
    total: int
    page: int
    per_page: int
    total_pages: int
    items: list[T] | None

class BaseFilter(BaseModel, Generic[T]):
    """Filtro base que pode ser extendido para cada modelo específico."""
    pass

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, description="Número da página")
    per_page: int = Field(10, ge=1, le=100, description="Registros por página")


class SortingParams(BaseModel):
    sort_by: str
    order: str


class StringFilterField(BaseModel):
    operator: str = Field(
        "eq",
        description="Operador para filtrar. Opções: \n"
        "- `eq`: Igual a\n"
        "- `neq`: Diferente de\n"
        "- `contains`: Contém\n"
        "- `not_contains`: Não contém",
        examples=["eq", "contains", "neq", "not_contains"],
    )
    value: str | None = Field(
        None,
        description="Valor a ser filtrado",
    )


class NumberFilterField(BaseModel):
    operator: str = Field(
        "eq",
        description="Operador para filtrar. Opções: \n"
        "- `eq`: Igual a\n"
        "- `neq`: Diferente de\n"
        "- `contains`: Contém\n"
        "- `not_contains`: Não contém",
        examples=["eq", "contains", "neq", "not_contains"],
    )
    value: int | None = Field(
        None,
        description="Valor a ser filtrado",
    )

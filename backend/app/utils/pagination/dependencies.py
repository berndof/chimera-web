from typing import TypeVar

from fastapi import Query

from app.database.dependencies import Base
from app.utils.pagination.schemas import SortingParams

T = TypeVar("T", bound="Base")


""" def apply_filters(
    query: Select[Any], model: type[Base], filters: dict[str, dict[str, Any]]
) -> Select[Any]:
    Aplica os filtros recebidos na query.
    conditions: list[BinaryExpression[Any]] = []

    for field, rule in filters.items():+
        operator_name = rule.get("operator", "eq")  # operador padrão
        value = rule.get("value")
        operator_func = OPERATORS.get(operator_name)
        if operator_func and hasattr(model, field):
            column = getattr(model, field)
            conditions.append(operator_func(column, value))
    if conditions:
        query = query.where(and_(*conditions))
    return query """

def get_sorting_params(allowed_fields: list[str]):
    """
    Fábrica de dependências para ordenação.
    Permite definir dinamicamente quais campos são permitidos para ordenação.
    """

    def dependency(
        sort_by: str = Query(
            allowed_fields[0],
            regex=f"^({'|'.join(allowed_fields)})$",
            description="Ordenar por",
        ),
        order: str = Query("asc", regex="^(asc|desc)$", description="Ordem"),
    ) -> SortingParams:
        return SortingParams(sort_by=sort_by, order=order)

    return dependency

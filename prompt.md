veja como adiciono filtros nativamente as rotas de api dos meus modelos, 

tenho o modelo base 
```python
# app.database.dependencies.py
class Base(DeclarativeBase):
    # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#preventing-implicit-io-when-using-asyncsession
    __mapper_args__ = {"eager_defaults": True}

class SQLBaseModel(Base, UUIDMixin, TimeStampMixin, SoftDeleteMixin):
    """
    Base model for SQLAlchemy ORM.
    """
    __abstract__ = True
```

que herda alguns mixins 
```python
class SoftDeleteMixin:
    """
    Mixin para Soft Delete.

    - A coluna `deleted_at` armazena a data/hora em que o registro foi marcado como deletado.
      Se for `None`, o registro está ativo.
    - O método `soft_delete` marca o registro como deletado sem removê-lo do banco.
    - O método `restore` restaura o registro para o estado ativo.
    - O método de classe `filter_active` pode ser usado para filtrar registros ativos.
    """
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    def soft_delete(self) -> None:
        """
        Realiza o soft delete do registro.
        Em vez de remover, atualiza a coluna `deleted_at` com o timestamp atual.
        """
        self.deleted_at = func.now()
        return

    def restore(self) -> None:
        """
        Restaura o registro previamente marcado como deletado.
        """
        self.deleted_at = None

    @property
    def is_active(self) -> bool:
        """
        Verifica se o registro está ativo (não deletado).
        """
        return self.deleted_at is None

    @classmethod
    def filter_active(cls, query):
        """
        Adiciona um filtro para retornar apenas os registros ativos (não deletados).
        """
        return query.filter(cls.deleted_at.is_(None))


class TimeStampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now()
    )

class UUIDMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True, unique=True
    )
```
e tenho os meus tipos base 

```python
T = TypeVar("T", bound="SQLBaseModel")
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

    async def soft_delete(self, obj: T) -> None:
        """
        Realiza o soft delete do objeto.
        """
        obj.soft_delete()
        self.logger.debug(f"Soft deleted {obj}")
        await self.save(obj)
    
    @abstractmethod
    async def create(self, obj_in: BaseSchema) -> T:
        """
        Cria um novo objeto no banco de dados.
        """
        ...

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

    class BaseSchema(BaseModel, Generic[T]):
        model_config = ConfigDict(from_attributes=True)
```
partindo disso crio a minha rota

```python
@router.post("/list")
async def user_list(
    service: UserService = Depends(user_service),
    pagination: PaginationParams = Depends(),
    sorting: SortingParams = Depends(
        get_sorting_params(
            ["username", "created_at", "updated_at", "first_name", "last_name"]
        )
    ),
    filters: UserFilter = Depends(),
):
    response = await service.get_list(
        response_schema=UserPublic,
        page=pagination.page,
        per_page=pagination.per_page,
        sort_by=sorting.sort_by,
        order=sorting.order,
        filters=filters,
    )
    _logger.info(f"User list response: {response}")
    return response
```

a implementação do repositorio é a criada no BaseRepository e no service a padrão também 

tenho de pagination o seguinte 

```python
def apply_filters(
    query: Select[Any], model: type[Base], filters: dict[str, dict[str, Any]]
) -> Select[Any]:
    """
    Aplica os filtros recebidos na query.
    """
    conditions: list[BinaryExpression[Any]] = []

    for field, rule in filters.items():
        operator_name = rule.get("operator", "eq")  # operador padrão
        value = rule.get("value")
        operator_func = OPERATORS.get(operator_name)
        if operator_func and hasattr(model, field):
            column = getattr(model, field)
            conditions.append(operator_func(column, value))
    if conditions:
        query = query.where(and_(*conditions))
    return query

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

class Operators:
    """Classe que encapsula operadores para filtros SQLAlchemy."""

    @staticmethod
    def eq(column: InstrumentedAttribute[Any], value: Any) -> BinaryExpression[Any]:
        """Igualdade."""
        return column == value

    @staticmethod
    def neq(column: InstrumentedAttribute[Any], value: Any) -> BinaryExpression[Any]:
        """Diferente."""
        return column != value

    @staticmethod
    def contains(
        column: InstrumentedAttribute[Any], value: str
    ) -> BinaryExpression[Any]:
        """Contém (case insensitive)."""
        return column.ilike(f"%{value}%")

    @staticmethod
    def not_contains(
        column: InstrumentedAttribute[Any], value: str
    ) -> BinaryExpression[Any]:
        """Não contém (case insensitive)."""
        return ~column.ilike(f"%{value}%")

    @staticmethod
    def gt(column: InstrumentedAttribute[Any], value: Any) -> BinaryExpression[Any]:
        """Maior que."""
        return column > value

    @staticmethod
    def lt(column: InstrumentedAttribute[Any], value: Any) -> BinaryExpression[Any]:
        """Menor que."""
        return column < value

# Mapeamento de operadores com tipagem corrigida
OPERATORS: dict[
    str, Callable[[InstrumentedAttribute[Any], Any], BinaryExpression[Any]]
] = {
    "eq": Operators.eq,
    "neq": Operators.neq,
    "contains": Operators.contains,
    "not_contains": Operators.not_contains,
    "gt": Operators.gt,
    "lt": Operators.lt,
}


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

```

e o Filter que uso para o user é 
```python
class UserFilter(BaseFilter[UserBase]):
    username: StringFilterField | None = None
    email: StringFilterField | None = None
    first_name: StringFilterField | None = None
    last_name: StringFilterField | None = None
```

queria ver se não consigo aplicar os filtros de alguma maneira mais eficiente
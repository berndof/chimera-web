
1. Resposta com Meta-informação
Vamos alterar a rota para retornar uma estrutura mais rica:

```python
from fastapi import APIRouter, Depends, Query
from typing import List

from .schemas import RoleRead, PaginatedResponse
from .repository import RoleRepository, role_repository

router = APIRouter()

@router.get("/roles", response_model=PaginatedResponse[RoleRead])
async def get_roles(
    page: int = Query(1, ge=1, description="Número da página"),
    per_page: int = Query(10, ge=1, le=100, description="Registros por página"),
    role_repo: RoleRepository = Depends(role_repository)
):
    paginated_roles = await role_repo.get_paginated(page=page, per_page=per_page)
    return paginated_roles
```

2. Modelo PaginatedResponse (schemas.py)
```python
from typing import Generic, List, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")

class PaginatedResponse(GenericModel, Generic[T]):
    total: int
    page: int
    per_page: int
    total_pages: int
    items: List[T]
```

3. Método get_paginated no Repositório
```python
from typing import List
from sqlalchemy.future import select

async def get_paginated(self, page: int = 1, per_page: int = 10):
    offset = (page - 1) * per_page

    # Contar total de registros
    count_query = select(func.count()).select_from(self.model)
    total_result = await self.session.execute(count_query)
    total = total_result.scalar_one()

    # Buscar registros paginados
    query = select(self.model).offset(offset).limit(per_page)
    result = await self.session.execute(query)
    items = result.scalars().all()

    total_pages = (total + per_page - 1) // per_page  # Cálculo do total de páginas

    return {
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "items": items
    }
```   
4. Exemplo de Resposta
json
Copiar
Editar
{
  "total": 150,
  "page": 1,
  "per_page": 10,
  "total_pages": 15,
  "items": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "name": "admin",
      "description": "Administrador do sistema"
    },
    ...
  ]
}


1. Ajuste na Rota (routes.py)
Adicionaremos parâmetros sort_by e order:

```python
from fastapi import APIRouter, Depends, Query
from typing import List

from .schemas import RoleRead, PaginatedResponse
from .repository import RoleRepository, role_repository

router = APIRouter()

@router.get("/roles", response_model=PaginatedResponse[RoleRead])
async def get_roles(
    page: int = Query(1, ge=1, description="Número da página"),
    per_page: int = Query(10, ge=1, le=100, description="Registros por página"),
    sort_by: str = Query("name", regex="^(name|created_at)$", description="Ordenar por 'name' ou 'created_at'"),
    order: str = Query("asc", regex="^(asc|desc)$", description="Ordem 'asc' ou 'desc'"),
    role_repo: RoleRepository = Depends(role_repository)
):
    paginated_roles = await role_repo.get_paginated(
        page=page, per_page=per_page, sort_by=sort_by, order=order
    )
    return paginated_roles
```

2. Ajuste no Repositório (get_paginated)
```python
from typing import List
from sqlalchemy.future import select
from sqlalchemy import asc, desc, func

async def get_paginated(
    self,
    page: int = 1,
    per_page: int = 10,
    sort_by: str = "name",
    order: str = "asc"
):
    offset = (page - 1) * per_page

    # Total de registros
    count_query = select(func.count()).select_from(self.model)
    total_result = await self.session.execute(count_query)
    total = total_result.scalar_one()

    # Ordenamento
    sort_column = getattr(self.model, sort_by)
    order_func = asc if order == "asc" else desc

    # Query paginada
    query = select(self.model).order_by(order_func(sort_column)).offset(offset).limit(per_page)
    result = await self.session.execute(query)
    items = result.scalars().all()

    total_pages = (total + per_page - 1) // per_page

    return {
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "items": items
    }
```



Você disse:
adicione as melhorias também 
O ChatGPT disse:
Memória atualizada
Vamos aprimorar a paginação com as melhorias desejadas: ordenação por múltiplos campos e cache para melhorar a performance.

1. Ordenação por Múltiplos Campos
Agora, o parâmetro sort_by pode aceitar vários campos separados por vírgulas, e order pode definir a ordem para cada campo.

Rota Atualizada (routes.py)
python
Copiar
Editar
from fastapi import APIRouter, Depends, Query
from typing import List

from .schemas import RoleRead, PaginatedResponse
from .repository import RoleRepository, role_repository

router = APIRouter()

@router.get("/roles", response_model=PaginatedResponse[RoleRead])
async def get_roles(
    page: int = Query(1, ge=1, description="Número da página"),
    per_page: int = Query(10, ge=1, le=100, description="Registros por página"),
    sort_by: str = Query("name", description="Campos para ordenar, separados por vírgula. Ex: 'name,created_at'"),
    order: str = Query("asc", description="Ordem correspondente para cada campo: 'asc' ou 'desc'. Ex: 'asc,desc'"),
    role_repo: RoleRepository = Depends(role_repository)
):
    paginated_roles = await role_repo.get_paginated(
        page=page, per_page=per_page, sort_by=sort_by, order=order
    )
    return paginated_roles
2. Ajuste no Repositório (get_paginated)
python
Copiar
Editar
from typing import List
from sqlalchemy.future import select
from sqlalchemy import asc, desc, func

async def get_paginated(
    self,
    page: int = 1,
    per_page: int = 10,
    sort_by: str = "name",
    order: str = "asc"
):
    offset = (page - 1) * per_page

    # Total de registros
    count_query = select(func.count()).select_from(self.model)
    total_result = await self.session.execute(count_query)
    total = total_result.scalar_one()

    # Processar múltiplos campos de ordenação
    sort_fields = sort_by.split(",")
    order_directions = order.split(",")
    
    order_criteria = []
    
    for i, field in enumerate(sort_fields):
        field = field.strip()
        direction = order_directions[i] if i < len(order_directions) else "asc"
        
        sort_column = getattr(self.model, field, None)
        if not sort_column:
            raise ValueError(f"Campo inválido para ordenação: '{field}'")
        
        order_func = asc if direction == "asc" else desc
        order_criteria.append(order_func(sort_column))

    # Query com ordenação e paginação
    query = select(self.model).order_by(*order_criteria).offset(offset).limit(per_page)
    result = await self.session.execute(query)
    items = result.scalars().all()

    total_pages = (total + per_page - 1) // per_page

    return {
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "items": items
    }
3. Cache para Melhorar Performance
Usaremos o cache para resultados frequentemente acessados. Podemos utilizar o cachetools para cache in-memory.

Instalação do cachetools
bash
Copiar
Editar
pip install cachetools
Cache no Repositório (repository.py)
python
Copiar
Editar
from cachetools import TTLCache, cached

# Cache com TTL de 60 segundos e até 100 registros
cache = TTLCache(maxsize=100, ttl=60)

@cached(cache)
async def get_paginated(
    self,
    page: int = 1,
    per_page: int = 10,
    sort_by: str = "name",
    order: str = "asc"
):
    offset = (page - 1) * per_page

    count_query = select(func.count()).select_from(self.model)
    total_result = await self.session.execute(count_query)
    total = total_result.scalar_one()

    sort_fields = sort_by.split(",")
    order_directions = order.split(",")

    order_criteria = []

    for i, field in enumerate(sort_fields):
        field = field.strip()
        direction = order_directions[i] if i < len(order_directions) else "asc"
        
        sort_column = getattr(self.model, field, None)
        if not sort_column:
            raise ValueError(f"Campo inválido para ordenação: '{field}'")
        
        order_func = asc if direction == "asc" else desc
        order_criteria.append(order_func(sort_column))

    query = select(self.model).order_by(*order_criteria).offset(offset).limit(per_page)
    result = await self.session.execute(query)
    items = result.scalars().all()

    total_pages = (total + per_page - 1) // per_page

    return {
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "items": items
    }
4. Teste a Rota
Chamada para múltiplos campos com cache:

pgsql
Copiar
Editar
GET /roles?page=1&per_page=10&sort_by=name,created_at&order=asc,desc
5. Melhorias Possíveis
Cache distribuído com Redis para ambientes distribuídos.
Filtragem com critérios adicionais, como description.
Configuração TTL por ambiente, melhorando a performance em produção.

from fastapi import APIRouter, Depends

from app.modules.item.service import ItemService

from .dependencies import item_service

router = APIRouter()


@router.get("/")
def item_router():
    return "Hello Item"


@router.post("/create")
async def item_create(
    service: ItemService = Depends(item_service),
):
    return await service.get_by_name("teste")

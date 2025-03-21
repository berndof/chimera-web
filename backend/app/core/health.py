from fastapi import APIRouter, Depends

from app.core.schemas import HealthResponse

router = APIRouter(prefix="/health", tags=["health"])

class HealthService:
    async def check_health(self):
        # lógica de checagem TODO
        return HealthResponse(status="ok", message="Healthy Service")


async def health_service():
    return HealthService()


@router.get("/", response_model=HealthResponse)
async def health(health_service: HealthService = Depends(health_service)):
    return await health_service.check_health()


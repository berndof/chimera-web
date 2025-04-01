from fastapi import FastAPI

from app.core.auth.routes import router as auth_router
from app.core.role.routes import router as role_router
from app.core.user.routes import router as user_router

def register(app: FastAPI):
    """
    Register the core module with the FastAPI app.
    """
    app.include_router(auth_router)
    app.include_router(role_router)
    app.include_router(user_router)
    
    return
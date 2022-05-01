from fastapi import APIRouter

from api.v1.routes import health, internal

api_router = APIRouter()

api_router.include_router(
    health.router, prefix="/healthcheck", tags=["health"])
api_router.include_router(
    internal.router, prefix="", tags=["internal"])
    

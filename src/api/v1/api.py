from fastapi import APIRouter

from api.v1.routes import health, continent, country

api_router = APIRouter()

api_router.include_router(
    health.router, prefix="/healthcheck", tags=["health"])
api_router.include_router(
    continent.router, prefix="/continents", tags=["continent"])
api_router.include_router(
    country.router, prefix="/countries", tags=["country"])

    

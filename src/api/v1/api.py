from fastapi import APIRouter

from api.v1.routes import health, continent, country, city

api_router = APIRouter()

api_router.include_router(
    health.router, prefix="/healthcheck", tags=["health"])
api_router.include_router(
    continent.router, prefix="/continent", tags=["continent"])
api_router.include_router(
    country.router, prefix="/country", tags=["country"])
api_router.include_router(
    city.router, prefix="/city", tags=["city"])

    

"""Central API router — registers all feature module routers."""
from fastapi.routing import APIRouter

from fast_api.web.api.auth import router as auth_router
from fast_api.web.api.monitoring import router as monitoring_router
from fast_api.web.api.weather import router as weather_router

api_router = APIRouter()

api_router.include_router(monitoring_router, prefix="/monitoring", tags=["monitoring"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(weather_router, prefix="/weather", tags=["weather"])

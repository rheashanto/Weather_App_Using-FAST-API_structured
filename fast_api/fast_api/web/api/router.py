"""API router - registers all route modules."""
from fastapi.routing import APIRouter

from fast_api.web.api import monitoring
from fast_api.web.api.auth import router as auth_router
from fast_api.web.api.weather import router as weather_router

api_router = APIRouter()

# Existing template routes
api_router.include_router(monitoring.router)

# Weather app routes
api_router.include_router(auth_router)
api_router.include_router(weather_router)
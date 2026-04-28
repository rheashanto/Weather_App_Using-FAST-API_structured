"""FastAPI application factory."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fast_api.web.api.router import api_router
from fast_api.web.lifespan import lifespan_setup


def get_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    :return: configured FastAPI instance.
    """
    app = FastAPI(
        title="WeatherVault",
        lifespan=lifespan_setup,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    # Fix: explicit origins instead of wildcard + credentials
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:5500",
            "http://127.0.0.1:5500",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router=api_router, prefix="/api")
    return app

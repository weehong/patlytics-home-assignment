import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.config import get_settings
from routes.patent import PatentAPI

patent = PatentAPI()


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
    )

    cors_origins = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
    cors_origins = [origin.strip() for origin in cors_origins if origin.strip()]

    if not cors_origins:
        cors_origins = ["http://localhost:5173"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    app.include_router(patent.router)

    return app


app = create_app()

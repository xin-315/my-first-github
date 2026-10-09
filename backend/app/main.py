"""
JC2001 Smart Study Assistant System PoC MVP
Main FastAPI Application Entrypoint
"""

import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.config import settings
from backend.app.routers.health import router as health_router
from backend.app.routers.quiz import router as quiz_router
from backend.app.routers.diagnose import router as diagnose_router

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("smartstudy_api")

def create_app() -> FastAPI:
    """FastAPI application factory."""
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="JC2001 Smart Study Assistant System (智学罗盘) PoC MVP API Service"
    )

    # 1. Global CORS Middleware for local browser and file:// protocol zero-barrier access
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"]
    )

    # 2. Register /api endpoints
    application.include_router(health_router, prefix="/api")
    application.include_router(quiz_router, prefix="/api")
    application.include_router(diagnose_router, prefix="/api")

    # 3. Mount frontend static directory at root / for single-port instant preview
    frontend_dir = settings.FRONTEND_DIR
    if frontend_dir.exists() and frontend_dir.is_dir():
        logger.info(f"Mounting static frontend directory from: {frontend_dir}")
        application.mount(
            "/",
            StaticFiles(directory=str(frontend_dir), html=True),
            name="frontend"
        )
    else:
        logger.warning(f"Frontend directory not found at {frontend_dir}; skipping static mount.")

    return application


app = create_app()

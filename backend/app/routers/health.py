"""
Health Check Router - GET /api/health
"""

from fastapi import APIRouter
from backend.app.config import settings
from backend.app.models.common import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check() -> HealthResponse:
    """
    Health probe endpoint returning service operational status.
    """
    return HealthResponse(
        status="ok",
        service=settings.SERVICE_ID,
        version=settings.VERSION,
        mode="dual-mode",
        has_api_key=settings.has_api_key
    )

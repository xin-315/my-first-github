"""
Health Check Router - GET /api/health and GET /api/health/llm
"""

from fastapi import APIRouter
from backend.app.config import settings
from backend.app.models.common import HealthResponse, LlmHealthResponse
from backend.app.services.llm_diagnostics import probe_llm_connectivity

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


@router.get("/health/llm", response_model=LlmHealthResponse, tags=["Health"])
async def llm_health_check() -> LlmHealthResponse:
    """
    Live LLM key probe - sends one minimal request to DashScope and reports whether the
    configured key actually works.

    `/api/health` only exposes a `has_api_key` boolean, which cannot distinguish a missing
    key from a revoked key, a rate limit or an unreachable network. This endpoint makes the
    difference explicit and classifies the failure, so the operator knows what to fix.

    It never raises: an unusable key is returned as data (`ok=false` plus a `kind` and a
    `suggestion`), never as a 5xx.
    """
    result = await probe_llm_connectivity()
    return LlmHealthResponse(
        ok=result.ok,
        kind=result.kind,
        message=result.message,
        model=result.model,
        endpoint=result.endpoint,
        api_key_masked=result.api_key_masked,
        latency_ms=result.latency_ms,
        status_code=result.status_code,
        retryable=result.retryable,
        suggestion=result.suggestion,
        details=result.details,
    )

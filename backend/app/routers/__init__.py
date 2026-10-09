"""
Routers package exports
"""

from backend.app.routers.health import router as health_router
from backend.app.routers.quiz import router as quiz_router
from backend.app.routers.diagnose import router as diagnose_router

__all__ = ["health_router", "quiz_router", "diagnose_router"]

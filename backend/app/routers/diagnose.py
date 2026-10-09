"""
Diagnostic Router - POST /api/diagnose
"""

from fastapi import APIRouter
from backend.app.models.diagnose import DiagnoseRequest, DiagnoseResponse
from backend.app.services.diagnostic_service import diagnostic_service

router = APIRouter()


@router.post("/diagnose", response_model=DiagnoseResponse, tags=["Diagnose"])
async def diagnose_option_selection(req: DiagnoseRequest) -> DiagnoseResponse:
    """
    Evaluate student's answer choice against cognitive distractor traps.
    Returns Socratic guidance, prerequisite theorems, and dynamic score adjustments.
    Operates in dual-mode with guaranteed zero unhandled 500 exceptions.
    """
    return await diagnostic_service.diagnose_answer(req)

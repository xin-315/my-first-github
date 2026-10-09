"""
Quiz Router - GET /api/quiz
"""

from typing import List, Optional
from fastapi import APIRouter, Query
from backend.app.models.quiz import QuizItem
from backend.app.services.quiz_service import quiz_service

router = APIRouter()


@router.get("/quiz", response_model=List[QuizItem], tags=["Quiz"])
def get_quiz_questions(
    subject: Optional[str] = Query(None, description="Discipline code or alias (e.g. econ, economics, cs, law, se)"),
    limit: Optional[int] = Query(None, ge=1, description="Optional maximum number of questions to return")
) -> List[QuizItem]:
    """
    Fetch curated question bank.
    Supports discipline filtering and alias normalization (e.g. 'economics' -> 'econ').
    """
    return quiz_service.get_questions(subject=subject, limit=limit)

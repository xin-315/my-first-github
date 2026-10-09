"""
Quiz Service - Question Management and Subject Alias Normalization
"""

from typing import List, Optional, Dict
from backend.app.models.quiz import QuizItem
from backend.app.data.seed_questions import SEED_QUESTIONS

SUBJECT_ALIASES: Dict[str, str] = {
    # Economics
    "econ": "econ",
    "economics": "econ",
    "econometrics": "econ",
    "计量经济学": "econ",
    "计量": "econ",
    "经管": "econ",
    
    # Computer Science
    "cs": "cs",
    "computer_science": "cs",
    "computer-science": "cs",
    "computerscience": "cs",
    "comp_sci": "cs",
    "计算机体系结构": "cs",
    "计算机科学": "cs",
    "计组": "cs",
    "计算机": "cs",
    
    # Law
    "law": "law",
    "civil_law": "law",
    "civil-law": "law",
    "civillaw": "law",
    "民商法学": "law",
    "民商法": "law",
    "法学": "law",
    "民法典": "law",
    
    # Software Engineering
    "se": "se",
    "software_engineering": "se",
    "software-engineering": "se",
    "softwareengineering": "se",
    "软件工程": "se",
    "软工": "se",
}


class QuizService:
    """Service handling question lookups, filtering, and subject normalizations."""

    def __init__(self, questions: Optional[List[QuizItem]] = None):
        self._questions = list(questions) if questions is not None else list(SEED_QUESTIONS)
        self._index_by_id: Dict[str, QuizItem] = {}
        for q in self._questions:
            self._index_by_id[q.id] = q
            if q.question_id:
                self._index_by_id[q.question_id] = q

    @staticmethod
    def normalize_subject(subject: Optional[str]) -> Optional[str]:
        """Normalize subject name or alias to canonical code (econ, cs, law, se)."""
        if not subject:
            return None
        cleaned = subject.strip().lower()
        return SUBJECT_ALIASES.get(cleaned, cleaned)

    def get_questions(self, subject: Optional[str] = None, limit: Optional[int] = None) -> List[QuizItem]:
        """
        Fetch questions with optional subject filtering and limit.
        If subject is given, resolves aliases (e.g. 'economics' -> 'econ').
        """
        if not subject:
            result = list(self._questions)
        else:
            canonical = self.normalize_subject(subject)
            result = [q for q in self._questions if q.subject.lower() == canonical]
            # Fallback if no questions matched canonical: return all or check substring
            if not result:
                result = [q for q in self._questions if canonical in q.subject.lower()]

        if limit is not None and limit > 0:
            result = result[:limit]

        return result

    def get_question_by_id(self, question_id: str) -> Optional[QuizItem]:
        """Look up a specific question by question ID."""
        if not question_id:
            return None
        target = str(question_id).strip()
        # Direct lookup
        if target in self._index_by_id:
            return self._index_by_id[target]
        # Case-insensitive or normalized lookup
        for q in self._questions:
            if q.id.lower() == target.lower() or (q.question_id and q.question_id.lower() == target.lower()):
                return q
        return None


# Global singleton instance
quiz_service = QuizService()

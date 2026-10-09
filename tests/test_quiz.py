"""
Quiz Endpoint Verification Suite (GET /api/quiz)
Covers Tier 1 (Functional & Schema), Tier 2 (Boundaries, Aliasing & Adversarial),
and Tier 3 (Cross-Subject Consistency).
"""

import pytest
from typing import List, Dict, Any
from starlette.testclient import TestClient


def validate_quiz_item_schema(item: Dict[str, Any]) -> None:
    """
    Helper function to assert that a quiz item dictionary conforms to the QuizItem contract.
    Supports either list of OptionItem or dict of options.
    """
    assert isinstance(item, dict), "Quiz item must be a dictionary"
    
    # Check ID field (id or question_id)
    q_id = item.get("id") or item.get("question_id") or item.get("questionId")
    assert q_id and isinstance(q_id, str), f"Quiz item must have non-empty id/question_id: {item}"

    # Check subject
    subject = item.get("subject")
    assert subject and isinstance(subject, str), f"Quiz item must have a valid subject: {item}"

    # Check stem
    stem = item.get("stem")
    assert stem and isinstance(stem, str) and len(stem.strip()) > 0, "Stem must be a non-empty string"

    # Check options
    options = item.get("options")
    assert options is not None, "Options must be present in QuizItem"
    
    if isinstance(options, dict):
        assert len(options) >= 2, "Options dictionary must contain at least 2 choices"
        for opt_key, opt_text in options.items():
            assert isinstance(opt_key, str)
            assert isinstance(opt_text, str) and len(opt_text.strip()) > 0
    elif isinstance(options, list):
        assert len(options) >= 2, "Options list must contain at least 2 choices"
        keys = []
        for opt in options:
            assert isinstance(opt, dict), "Each option item must be a dict"
            key = opt.get("key")
            assert key and isinstance(key, str), f"Option key missing in {opt}"
            keys.append(key)
            text = opt.get("text")
            assert text and isinstance(text, str), f"Option text missing in {opt}"
        # Standard multiple choice usually includes A, B, C, D
        assert "A" in keys and "B" in keys, "Options should include at least 'A' and 'B'"
    else:
        pytest.fail(f"Options format invalid: {type(options)}")


# -----------------------------------------------------------------------------
# Tier 1: Functional & Schema Tests
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("subject_query", ["economics", "econ", "cs", "law", "se"])
def test_quiz_endpoint_valid_subjects(client: TestClient, subject_query: str):
    """
    Tier 1: Verify querying valid subjects returns 200 OK and valid QuizItem list.
    Authority: ORIGINAL_REQUEST.md R1 & PROJECT.md Interface Contracts.
    """
    response = client.get(f"/api/quiz?subject={subject_query}")
    assert response.status_code == 200, (
        f"Failed to fetch quiz for subject '{subject_query}': {response.status_code} {response.text}"
    )

    questions = response.json()
    assert isinstance(questions, list), f"Expected list of questions for '{subject_query}', got {type(questions)}"
    assert len(questions) > 0, f"Expected non-empty questions list for subject '{subject_query}'"

    for q in questions:
        validate_quiz_item_schema(q)


def test_quiz_default_subject_query(client: TestClient):
    """
    Tier 1: Verify invoking /api/quiz with no query parameters returns default question set without error.
    """
    response = client.get("/api/quiz")
    assert response.status_code == 200, f"Expected 200 OK for default quiz endpoint, got {response.status_code}"
    questions = response.json()
    assert isinstance(questions, list)
    assert len(questions) > 0
    for q in questions:
        validate_quiz_item_schema(q)


# -----------------------------------------------------------------------------
# Tier 2: Subject Aliasing & Normalization
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("alias_pair", [
    ("economics", "econ"),
    ("computer_science", "cs"),
    ("software_engineering", "se")
])
def test_quiz_subject_aliasing(client: TestClient, alias_pair: tuple):
    """
    Tier 2: Verify subject aliases map to the same question set.
    e.g., 'economics' <-> 'econ', 'computer_science' <-> 'cs'.
    """
    full_name, alias = alias_pair
    resp_full = client.get(f"/api/quiz?subject={full_name}")
    resp_alias = client.get(f"/api/quiz?subject={alias}")

    assert resp_full.status_code == 200, f"Failed for full name {full_name}"
    assert resp_alias.status_code == 200, f"Failed for alias {alias}"

    data_full = resp_full.json()
    data_alias = resp_alias.json()

    # Extract question IDs from both
    ids_full = [q.get("id") or q.get("question_id") for q in data_full]
    ids_alias = [q.get("id") or q.get("question_id") for q in data_alias]

    assert ids_full == ids_alias, (
        f"Alias '{alias}' and full name '{full_name}' should return identical question IDs. "
        f"Got {ids_full} vs {ids_alias}"
    )


@pytest.mark.parametrize("case_variant", ["ECONOMICS", "Econ", "CS", "Law", "SE"])
def test_quiz_subject_case_insensitivity(client: TestClient, case_variant: str):
    """
    Tier 2: Verify subject parameter is case-insensitive.
    """
    response = client.get(f"/api/quiz?subject={case_variant}")
    assert response.status_code == 200
    questions = response.json()
    assert isinstance(questions, list)
    assert len(questions) > 0


# -----------------------------------------------------------------------------
# Tier 2 & 3: Boundary & Adversarial Tests
# -----------------------------------------------------------------------------

def test_quiz_invalid_subject_graceful_handling(client: TestClient):
    """
    Tier 2 Boundary: Querying an unknown subject must return either an empty list
    or a 404 structured response, never crashing with 500 Internal Server Error.
    """
    response = client.get("/api/quiz?subject=quantum_alchemy_astrology_999")
    assert response.status_code in [200, 404], (
        f"Unknown subject should return 200 (empty list) or 404, not {response.status_code}"
    )
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0, "Unknown subject should return 0 questions"


@pytest.mark.parametrize("adversarial_input", [
    "",                             # Empty string
    "   ",                          # Whitespace only
    "<script>alert(1)</script>",    # XSS injection attempt
    "' OR '1'='1",                  # SQLi attempt
    "../etc/passwd",                # Path traversal attempt
    "a" * 256                       # Extremely long parameter
])
def test_quiz_adversarial_subject_inputs(client: TestClient, adversarial_input: str):
    """
    Tier 2 Adversarial: Verify malformed or hostile subject queries do not trigger unhandled 500 errors.
    """
    response = client.get("/api/quiz", params={"subject": adversarial_input})
    assert response.status_code in [200, 400, 404, 422], (
        f"Adversarial subject query caused unexpected status {response.status_code}: {response.text}"
    )
    assert response.status_code != 500, "Server must not crash with 500 on hostile input"

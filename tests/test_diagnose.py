"""
Diagnostic Endpoint Verification Suite (POST /api/diagnose)
Covers Tier 1 (Functional & Schema Contracts), Tier 2 (Boundaries & Negative Inputs),
Tier 3 (Resilient Fallback Mode & Timeout Simulation), and Tier 4 (Socratic Quality).
"""

import pytest
from unittest.mock import patch
from starlette.testclient import TestClient


# -----------------------------------------------------------------------------
# Tier 1: Functional & Schema Contracts
# -----------------------------------------------------------------------------

def test_diagnose_distractor_trap_offline_fallback(client: TestClient, econ_distractor_payload: dict):
    """
    Tier 1: Verify selecting an incorrect option returns is_correct=False,
    extracts the pre-tagged misconception trap, returns Socratic guidance,
    and sets fallback_mode=True when offline.
    Authority: ORIGINAL_REQUEST.md R1, R3 & PROJECT.md Section 53 Contract.
    """
    response = client.post("/api/diagnose", json=econ_distractor_payload)
    assert response.status_code == 200, (
        f"Diagnosis failed with status {response.status_code}: {response.text}"
    )

    data = response.json()
    assert isinstance(data, dict), "Diagnose response must be a JSON object"

    # Verify correctness flag
    is_correct = data.get("is_correct") if "is_correct" in data else data.get("isCorrect")
    assert is_correct is False, f"Expected is_correct=False for distractor option, got {is_correct}"

    # Verify trap attribution
    trap_text = data.get("trap_name") or data.get("trap_title") or data.get("trapName") or data.get("trapTitle")
    assert trap_text and isinstance(trap_text, str) and len(trap_text) > 0, (
        f"Expected non-empty trap attribution in {data}"
    )

    # Verify prerequisite concept attribution
    concept_text = (
        data.get("concept_name") 
        or data.get("conceptName") 
        or data.get("prerequisite") 
        or data.get("misconception")
    )
    assert concept_text and isinstance(concept_text, str) and len(concept_text) > 0, (
        f"Expected non-empty concept or prerequisite attribution in {data}"
    )

    # Verify Socratic guidance prompt
    socratic = (
        data.get("socratic_guidance") 
        or data.get("socraticGuidance") 
        or data.get("socratic_hint") 
        or data.get("socraticHint")
    )
    assert socratic and isinstance(socratic, str) and len(socratic) > 0, (
        f"Expected non-empty Socratic guidance in {data}"
    )

    # Verify offline fallback flag (since DASHSCOPE_API_KEY is clean in test env)
    fallback_mode = data.get("fallback_mode") if "fallback_mode" in data else data.get("fallbackMode")
    assert fallback_mode is True, f"Expected fallback_mode=True in offline test environment, got {fallback_mode}"


def test_diagnose_correct_option(client: TestClient, econ_correct_payload: dict):
    """
    Tier 1: Verify selecting the correct answer option returns is_correct=True with HTTP 200.
    """
    response = client.post("/api/diagnose", json=econ_correct_payload)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}: {response.text}"

    data = response.json()
    is_correct = data.get("is_correct") if "is_correct" in data else data.get("isCorrect")
    assert is_correct is True, f"Expected is_correct=True for correct answer, got {is_correct}"

    explanation = data.get("explanation")
    if explanation is not None:
        assert isinstance(explanation, str)


@pytest.mark.parametrize("payload_fixture_name", [
    "law_distractor_payload",
    "cs_distractor_payload",
    "se_distractor_payload"
])
def test_diagnose_multi_subject_distractors(client: TestClient, request, payload_fixture_name: str):
    """
    Tier 1 & 3: Cross-subject validation: verify diagnosis works across all core subjects
    (Law, Computer Science, Software Engineering) without 500 errors.
    """
    payload = request.getfixturevalue(payload_fixture_name)
    response = client.post("/api/diagnose", json=payload)
    assert response.status_code == 200, (
        f"Failed for subject payload {payload}: {response.status_code} {response.text}"
    )
    data = response.json()
    is_correct = data.get("is_correct") if "is_correct" in data else data.get("isCorrect")
    assert is_correct is False


# -----------------------------------------------------------------------------
# Tier 2: Boundary, Negative & Schema Validation Tests
# -----------------------------------------------------------------------------

def test_diagnose_missing_fields_unprocessable_entity(client: TestClient):
    """
    Tier 2 Negative: Request with invalid data structures must return HTTP 422 Unprocessable Entity.
    """
    # String instead of object payload
    resp_str = client.post("/api/diagnose", json="invalid_string_payload")
    assert resp_str.status_code == 422, f"Expected 422 for non-dict payload, got {resp_str.status_code}"

    # List instead of object payload
    resp_list = client.post("/api/diagnose", json=["invalid", "list"])
    assert resp_list.status_code == 422, f"Expected 422 for list payload, got {resp_list.status_code}"

    # Empty payload handled safely without 500 internal server error
    resp_empty = client.post("/api/diagnose", json={})
    assert resp_empty.status_code in [200, 422], f"Unexpected status {resp_empty.status_code}"
    assert resp_empty.status_code != 500, "Server must not crash with 500 on empty payload"


def test_diagnose_nonexistent_question_id(client: TestClient):
    """
    Tier 2 Boundary: Querying a non-existent question ID must return either 404
    or a structured error, NEVER crashing with 500 Internal Server Error.
    """
    payload = {"question_id": "nonexistent_question_9999", "selected_option": "A"}
    response = client.post("/api/diagnose", json=payload)
    assert response.status_code in [404, 400, 422, 200], (
        f"Server returned unexpected status {response.status_code}: {response.text}"
    )
    assert response.status_code != 500, "Server must not throw unhandled 500 for missing question"


def test_diagnose_camel_case_input_interoperability(client: TestClient):
    """
    Tier 2 Schema: Verify frontend camelCase payloads (questionId, selectedKey)
    are accepted transparently by the backend Pydantic models.
    """
    payload = {
        "questionId": "econ_1",
        "selectedKey": "A"
    }
    response = client.post("/api/diagnose", json=payload)
    assert response.status_code == 200, f"camelCase payload failed: {response.status_code} {response.text}"
    data = response.json()
    is_correct = data.get("is_correct") if "is_correct" in data else data.get("isCorrect")
    assert is_correct is False


# -----------------------------------------------------------------------------
# Tier 3: Resilient Fallback Under Network / Timeout Outage
# -----------------------------------------------------------------------------

def test_diagnose_resilience_under_mocked_network_outage(client: TestClient, monkeypatch: pytest.MonkeyPatch):
    """
    Tier 3 Resilience: Simulate external LLM network failure / timeout.
    The service must catch all external exceptions and fall back gracefully
    to local seed data with fallback_mode=True, returning HTTP 200 with ZERO 500 errors.
    Authority: ORIGINAL_REQUEST.md Acceptance Criteria & R3.
    """
    # Provide a mock key to trigger the LLM call branch
    monkeypatch.setenv("DASHSCOPE_API_KEY", "mock_key_for_timeout_test")

    # Mock external calls to raise a network timeout/exception
    with patch("httpx.AsyncClient.post", side_effect=Exception("Simulated External Network Timeout")):
        with patch("requests.post", side_effect=Exception("Simulated External Connection Error")):
            payload = {"question_id": "econ_1", "selected_option": "A"}
            response = client.post("/api/diagnose", json=payload)
            
            assert response.status_code == 200, (
                f"Expected resilient HTTP 200 fallback during network failure, got {response.status_code}: {response.text}"
            )
            data = response.json()
            fallback_flag = data.get("fallback_mode") if "fallback_mode" in data else data.get("fallbackMode")
            assert fallback_flag is True, "Response must signal fallback_mode=True on simulated outage"


# -----------------------------------------------------------------------------
# Tier 4: Socratic Guidance Pedagogical Quality
# -----------------------------------------------------------------------------

def test_diagnose_socratic_guidance_pedagogical_depth(client: TestClient, econ_distractor_payload: dict):
    """
    Tier 4 Socratic: Verify Socratic guidance contains substantial guiding thought
    and does not trivially state a raw error code.
    """
    response = client.post("/api/diagnose", json=econ_distractor_payload)
    assert response.status_code == 200
    data = response.json()

    socratic = (
        data.get("socratic_guidance") 
        or data.get("socraticGuidance") 
        or data.get("socratic_hint") 
        or data.get("socraticHint")
    )
    assert socratic is not None
    # Socratic guidance should be a reflective pedagogical question or hint (> 10 characters)
    assert len(socratic.strip()) >= 10, f"Socratic guidance '{socratic}' lacks sufficient depth"

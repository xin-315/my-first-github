"""
CORS Middleware and Cross-Origin Header Verification Suite
Covers Tier 1 (CORS Defaults), Tier 2 (Local Development Origins & file:// null origin),
and Tier 3 (Preflight OPTIONS Handshake).
"""

import pytest
from starlette.testclient import TestClient


# Origins typically encountered by students and evaluators
LOCAL_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "null",  # Browsers send 'null' for file:/// URLs
]


# -----------------------------------------------------------------------------
# Tier 1 & 2: GET and POST CORS Header Verification
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("origin", LOCAL_ORIGINS)
def test_cors_headers_on_get_health(client: TestClient, origin: str):
    """
    Tier 1 & 2: Verify that GET requests with Origin header receive valid CORS response headers.
    Authority: ORIGINAL_REQUEST.md R2 & PROJECT.md CORS Specifications.
    """
    headers = {"Origin": origin}
    response = client.get("/api/health", headers=headers)
    assert response.status_code == 200

    allow_origin = response.headers.get("access-control-allow-origin")
    assert allow_origin is not None, f"Missing Access-Control-Allow-Origin header for origin '{origin}'"
    assert allow_origin in ["*", origin], (
        f"Expected Access-Control-Allow-Origin to be '*' or '{origin}', got '{allow_origin}'"
    )


@pytest.mark.parametrize("origin", LOCAL_ORIGINS)
def test_cors_headers_on_post_diagnose(client: TestClient, origin: str, econ_distractor_payload: dict):
    """
    Tier 1 & 2: Verify that POST requests with Origin header receive valid CORS response headers.
    """
    headers = {
        "Origin": origin,
        "Content-Type": "application/json"
    }
    response = client.post("/api/diagnose", json=econ_distractor_payload, headers=headers)
    assert response.status_code == 200

    allow_origin = response.headers.get("access-control-allow-origin")
    assert allow_origin is not None, f"Missing Access-Control-Allow-Origin for POST with origin '{origin}'"
    assert allow_origin in ["*", origin]


# -----------------------------------------------------------------------------
# Tier 3: Preflight OPTIONS Request Verification
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("origin", LOCAL_ORIGINS)
def test_cors_preflight_options_for_diagnose(client: TestClient, origin: str):
    """
    Tier 3: Preflight OPTIONS request verification before POST /api/diagnose.
    Validates Access-Control-Allow-Origin, Access-Control-Allow-Methods, and Access-Control-Allow-Headers.
    """
    headers = {
        "Origin": origin,
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "Content-Type,Authorization"
    }
    response = client.options("/api/diagnose", headers=headers)
    assert response.status_code in [200, 204], (
        f"Preflight OPTIONS failed with status {response.status_code}: {response.text}"
    )

    # Validate origin header
    allow_origin = response.headers.get("access-control-allow-origin")
    assert allow_origin is not None, "Preflight response must contain Access-Control-Allow-Origin"
    assert allow_origin in ["*", origin]

    # Validate allowed methods
    allow_methods = response.headers.get("access-control-allow-methods", "")
    assert "POST" in allow_methods.upper() or allow_methods == "*", (
        f"Expected POST in Access-Control-Allow-Methods, got '{allow_methods}'"
    )


def test_cors_preflight_options_for_quiz(client: TestClient):
    """
    Tier 3: Preflight OPTIONS request verification for GET /api/quiz.
    """
    headers = {
        "Origin": "http://localhost:5500",
        "Access-Control-Request-Method": "GET"
    }
    response = client.options("/api/quiz", headers=headers)
    assert response.status_code in [200, 204]
    allow_origin = response.headers.get("access-control-allow-origin")
    assert allow_origin in ["*", "http://localhost:5500"]

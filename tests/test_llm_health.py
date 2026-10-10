"""
Live-LLM health probe verification suite (GET /api/health/llm + llm_diagnostics).

Covers Tier 1 (contract of the new endpoint), Tier 2 (failure classification boundaries),
Tier 3 (no-network resilience: the probe must never raise) and the text-safety helper used
to enforce the prompt's length budget.

The probe is exercised with a fake httpx client, so these tests need no network and no API key.
"""

import asyncio
import json

import httpx
import pytest

from backend.app.config import settings
from backend.app.services import llm_diagnostics
from backend.app.services.llm_diagnostics import (
    KIND_AUTH,
    KIND_NETWORK,
    KIND_NO_KEY,
    KIND_OK,
    KIND_PAYLOAD,
    KIND_RATE_LIMIT,
    KIND_SERVER,
    KIND_TIMEOUT,
    classify_llm_failure,
    kind_from_dashscope_code,
    mask_secret,
    probe_llm_connectivity,
    truncate_safely,
)


# ---------------------------------------------------------------------------
# Offline test doubles
# ---------------------------------------------------------------------------
class _FakeResponse:
    """Minimal stand-in for an httpx.Response."""

    def __init__(self, status_code: int, payload):
        self.status_code = status_code
        self._payload = payload
        self.text = json.dumps(payload, ensure_ascii=False) if not isinstance(payload, str) else payload

    def json(self):
        if isinstance(self._payload, str):
            raise ValueError("not JSON")
        return self._payload


class _FakeAsyncClient:
    """Stand-in for httpx.AsyncClient so the probe can run with no network."""

    def __init__(self, outcome, **_kwargs):
        self._outcome = outcome
        self.calls: list = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc_info):
        return False

    async def post(self, url, json=None, headers=None):
        self.calls.append({"url": url, "json": json, "headers": headers})
        if isinstance(self._outcome, Exception):
            raise self._outcome
        return self._outcome


def _dashscope_success_body(content: str = "OK") -> dict:
    """A DashScope text-generation success envelope."""
    return {
        "output": {"choices": [{"finish_reason": "stop", "message": {"role": "assistant", "content": content}}]},
        "usage": {"total_tokens": 5},
        "request_id": "test-request-id",
    }


@pytest.fixture
def fake_llm(monkeypatch):
    """
    Install an offline fake httpx client for llm_diagnostics and return an installer.

    Usage: `created = fake_llm(_FakeResponse(200, body))` then `created["client"].calls`.
    """
    def _install(outcome):
        created = {}

        def _factory(*args, **kwargs):
            client = _FakeAsyncClient(outcome, **kwargs)
            created["client"] = client
            return client

        monkeypatch.setattr(llm_diagnostics.httpx, "AsyncClient", _factory)
        return created

    return _install


@pytest.fixture
def with_api_key(monkeypatch):
    """Pretend a key is configured (settings is a module-level singleton, so patch the attribute)."""
    monkeypatch.setattr(settings, "QWEN_API_KEY", "sk-unit-test-key-0123456789abcdef")
    return settings


# ---------------------------------------------------------------------------
# Tier 1: endpoint contract
# ---------------------------------------------------------------------------
def test_health_llm_reports_missing_key(client):
    """
    Tier 1: with no key configured the endpoint must answer 200, name the `no_key` state and
    hand the operator an actionable suggestion - never a 5xx.
    """
    response = client.get("/api/health/llm")
    assert response.status_code == 200, f"expected 200, got {response.status_code}: {response.text}"

    data = response.json()
    assert data["ok"] is False
    assert data["kind"] == KIND_NO_KEY, f"expected no_key, got {data}"
    assert data["message"], "the probe must explain the outcome"
    assert data["suggestion"], "the probe must suggest a next step"
    assert data["retryable"] is False
    # camelCase interop, matching the rest of the API contract
    assert data["apiKeyMasked"] == data["api_key_masked"]
    assert "latency_ms" in data and "latencyMs" in data


def test_health_endpoint_unchanged(client):
    """Tier 1 regression: the pre-existing health probe keeps its contract."""
    data = client.get("/api/health").json()
    assert data["status"] == "ok"
    assert data["service"] == settings.SERVICE_ID
    assert data["has_api_key"] is False


def test_health_llm_masks_the_key_and_never_echoes_it(client, with_api_key, fake_llm):
    """Tier 1: the endpoint reports a masked key and must never leak the full value."""
    fake_llm(_FakeResponse(200, _dashscope_success_body()))

    data = client.get("/api/health/llm").json()
    assert data["ok"] is True and data["kind"] == KIND_OK

    masked = data["api_key_masked"]
    assert masked != with_api_key.QWEN_API_KEY
    assert with_api_key.QWEN_API_KEY not in json.dumps(data), "the full key leaked into the response"
    assert masked.startswith("sk-uni") and "***" in masked


def test_health_llm_success_path_reports_latency_and_sample(with_api_key, fake_llm):
    """Tier 1: a healthy call reports ok, latency and a small content sample."""
    created = fake_llm(_FakeResponse(200, _dashscope_success_body("OK")))

    result = asyncio.run(probe_llm_connectivity())

    assert result.ok is True
    assert result.kind == KIND_OK
    assert result.latency_ms is not None and result.latency_ms >= 0
    assert result.status_code == 200
    assert result.details.get("sample") == "OK"
    # the probe must talk to the configured endpoint with a bearer token
    call = created["client"].calls[0]
    assert call["url"] == settings.DASHSCOPE_URL
    assert call["headers"]["Authorization"] == f"Bearer {with_api_key.QWEN_API_KEY}"
    assert call["json"]["model"] == settings.QWEN_MODEL


# ---------------------------------------------------------------------------
# Tier 2: failure classification
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "status_code, expected_kind, expected_retryable",
    [
        (401, KIND_AUTH, False),
        (403, KIND_AUTH, False),
        (429, KIND_RATE_LIMIT, True),
        (404, KIND_PAYLOAD, False),
        (400, KIND_PAYLOAD, False),
        (500, KIND_SERVER, True),
        (503, KIND_SERVER, True),
    ],
)
def test_classify_http_status(status_code, expected_kind, expected_retryable):
    """Tier 2: every HTTP status maps to a stable kind and a correct retryable flag."""
    failure = classify_llm_failure(status_code=status_code, body='{"message":"x"}')
    assert failure.kind == expected_kind
    assert failure.retryable is expected_retryable
    assert failure.suggestion, "every failure kind must carry advice"


def test_classify_timeout_and_network_exceptions():
    """Tier 2: transport exceptions are distinguished from HTTP errors."""
    timeout = classify_llm_failure(exc=httpx.TimeoutException("timed out"))
    assert timeout.kind == KIND_TIMEOUT and timeout.retryable is True

    network = classify_llm_failure(exc=httpx.ConnectError("connection refused"))
    assert network.kind == KIND_NETWORK and network.retryable is True

    unknown = classify_llm_failure(exc=ValueError("boom"))
    assert unknown.kind == "unknown"


@pytest.mark.parametrize(
    "code, expected_kind",
    [
        ("InvalidApiKey", KIND_AUTH),
        ("invalid_api_key", KIND_AUTH),
        ("Arrearage", KIND_AUTH),
        ("Throttling.RateQuota", KIND_RATE_LIMIT),
        ("Throttling", KIND_RATE_LIMIT),
        ("ModelNotFound", KIND_PAYLOAD),
        ("InvalidParameter", KIND_PAYLOAD),
        ("SomethingElse", None),
        (None, None),
    ],
)
def test_dashscope_business_codes(code, expected_kind):
    """Tier 2: DashScope business codes are mapped, unknown codes fall through to None."""
    assert kind_from_dashscope_code(code) == expected_kind


def test_http_200_with_business_error_code_is_not_reported_as_ok(with_api_key, fake_llm):
    """
    Tier 2: DashScope can answer HTTP 200 while the body carries a business error. That must
    be classified as a failure, otherwise the health check would report a false positive.
    """
    fake_llm(_FakeResponse(200, {"code": "InvalidApiKey", "message": "Invalid API-key provided."}))

    result = asyncio.run(probe_llm_connectivity())

    assert result.ok is False
    assert result.kind == KIND_AUTH
    assert result.retryable is False


def test_http_200_with_no_content_is_a_payload_failure(with_api_key, fake_llm):
    """Tier 2: an empty 200 envelope is reported as a payload problem, not as success."""
    fake_llm(_FakeResponse(200, {"output": {}, "usage": {}}))

    result = asyncio.run(probe_llm_connectivity())

    assert result.ok is False
    assert result.kind == KIND_PAYLOAD


def test_rejected_key_is_classified_as_auth(with_api_key, fake_llm):
    """Tier 2: a revoked key surfaces as auth with the account advice attached."""
    fake_llm(_FakeResponse(401, {"code": "InvalidApiKey", "message": "Incorrect API key provided."}))

    result = asyncio.run(probe_llm_connectivity())

    assert result.ok is False
    assert result.kind == KIND_AUTH
    assert result.status_code == 401
    assert "bailian" in result.suggestion.lower()


# ---------------------------------------------------------------------------
# Tier 3: resilience - the probe must never raise
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "outcome, expected_kind",
    [
        (httpx.TimeoutException("read timeout"), KIND_TIMEOUT),
        (httpx.ConnectError("connection reset"), KIND_NETWORK),
        (httpx.ReadError("read error"), KIND_NETWORK),
        (RuntimeError("unexpected explosion"), "unknown"),
    ],
)
def test_probe_never_raises_on_transport_failures(with_api_key, fake_llm, outcome, expected_kind):
    """Tier 3: transport failures degrade to data, so the endpoint can never return a 5xx."""
    fake_llm(outcome)

    result = asyncio.run(probe_llm_connectivity())

    assert result.ok is False
    assert result.kind == expected_kind


def test_endpoint_stays_200_when_the_transport_explodes(client, with_api_key, fake_llm):
    """Tier 3: even a hard transport failure is reported as HTTP 200 with ok=false."""
    fake_llm(httpx.ConnectError("network down"))

    response = client.get("/api/health/llm")

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["ok"] is False and body["kind"] == KIND_NETWORK


def test_probe_without_key_reports_no_key(with_api_key, monkeypatch):
    """Tier 3: with no key the probe short-circuits without any network attempt."""
    monkeypatch.setattr(settings, "QWEN_API_KEY", "")

    result = asyncio.run(probe_llm_connectivity())

    assert result.ok is False
    assert result.kind == KIND_NO_KEY


# ---------------------------------------------------------------------------
# Text-safety helper (enforces the prompt's length budget)
# ---------------------------------------------------------------------------
def test_truncate_safely_keeps_short_text_untouched():
    assert truncate_safely("short guidance", 120) == "short guidance"
    assert truncate_safely(None) == ""
    assert truncate_safely("anything", 0) == ""


def test_truncate_safely_cuts_latin_text_on_a_word_boundary():
    """Latin text must not end in the middle of a word."""
    text = "Consider whether the unconditional expectation assumption still holds for this model"
    out = truncate_safely(text, 40)

    assert out.endswith("…")
    assert len(out) <= 41
    assert not out[:-1].endswith(" ") and out[:-1].split()[-1] in text.split(), out
    assert text.startswith(out[:-1])


def test_truncate_safely_handles_cjk_text_that_has_no_spaces():
    """CJK text has no spaces; it must still be trimmed to the budget, not dropped."""
    text = "请回忆相关先修定理的严格边界条件，并思考该选项是否真的满足题干所给的前提假设。"
    out = truncate_safely(text, 20)

    assert out.endswith("…")
    assert out[:-1] == text[:20]


def test_truncate_safely_collapses_whitespace():
    assert truncate_safely("line one\n\n   line two") == "line one line two"


def test_mask_secret_never_returns_the_input():
    for secret in ("", None, "short", "sk-0123456789abcdefghijklmnop"):
        masked = mask_secret(secret)
        if secret:
            assert masked != secret
            assert secret not in masked
        assert "***" in masked or masked == "(not configured)"


# ---------------------------------------------------------------------------
# CLI wrapper (backend/scripts/check_qwen_key.py)
# ---------------------------------------------------------------------------
def test_cli_exit_codes(monkeypatch, capsys):
    """The CLI must exit 0 when the key works and 1 when it does not, with a readable report."""
    from backend.scripts import check_qwen_key

    def _fake_ok():
        async def _coro():
            return llm_diagnostics.LLMProbeResult(
                ok=True, kind=KIND_OK, message="fine", model="qwen-turbo", latency_ms=12.0
            )

        return _coro()

    monkeypatch.setattr(check_qwen_key, "probe_llm_connectivity", _fake_ok)
    assert check_qwen_key.main() == 0
    assert "the key works" in capsys.readouterr().out

    def _fake_fail():
        async def _coro():
            return llm_diagnostics.LLMProbeResult(
                ok=False,
                kind=KIND_AUTH,
                message="rejected",
                suggestion="regenerate the key",
            )

        return _coro()

    monkeypatch.setattr(check_qwen_key, "probe_llm_connectivity", _fake_fail)
    assert check_qwen_key.main() == 1
    output = capsys.readouterr().out
    assert "regenerate the key" in output
    assert "fallback_mode=true" in output

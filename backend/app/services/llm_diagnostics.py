"""
LLM Diagnostics - API key health probing and failure classification.

Why this module exists
----------------------
`diagnostic_service` degrades silently to the local knowledge fallback whenever a live
Qwen call fails. That is the correct runtime behaviour, but it makes failures hard to
diagnose: a missing key, a revoked key, a rate limit and a dead network all look the same
from the outside, and `/api/health` only reports a `has_api_key` boolean.

This module makes those cases distinguishable:

* `classify_llm_failure()` turns an HTTP status, a DashScope error code or an exception
  into a stable machine-readable kind plus an actionable suggestion;
* `probe_llm_connectivity()` performs one minimal real request and reports whether the
  configured key actually works;
* `truncate_safely()` enforces the prompt's length budget without cutting a Latin word in
  half and without breaking CJK text (which has no spaces to cut on).

Consumed by `GET /api/health/llm` and by `backend/scripts/check_qwen_key.py`.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple

import httpx

from backend.app.config import settings

logger = logging.getLogger("llm_diagnostics")

# --- Failure kinds (stable identifiers, safe to assert on / alert on) ---------
KIND_OK = "ok"
KIND_NO_KEY = "no_key"
KIND_AUTH = "auth"
KIND_RATE_LIMIT = "rate_limit"
KIND_TIMEOUT = "timeout"
KIND_NETWORK = "network"
KIND_SERVER = "server"
KIND_PAYLOAD = "payload"
KIND_UNKNOWN = "unknown"

RETRYABLE_KINDS = frozenset({KIND_RATE_LIMIT, KIND_TIMEOUT, KIND_NETWORK, KIND_SERVER})

# Actionable, developer-facing advice per kind (the CLI and the endpoint both surface it).
SUGGESTIONS: Dict[str, str] = {
    KIND_OK: "No action needed; the live Qwen call path is working.",
    KIND_NO_KEY: (
        "Set QWEN_API_KEY (or DASHSCOPE_API_KEY) in .env, then restart the backend. "
        "Until then every diagnosis uses the offline fallback."
    ),
    KIND_AUTH: (
        "The key was rejected: check for a truncated copy-paste, an expired or reset key, "
        "an account without model access, or a key from a different provider. "
        "Regenerate it at https://bailian.console.aliyun.com/ ."
    ),
    KIND_RATE_LIMIT: (
        "Rate limited or out of quota: wait and retry, or raise the account quota. "
        "The service keeps serving offline diagnoses meanwhile."
    ),
    KIND_TIMEOUT: (
        "The call did not finish inside the configured timeout: check the network, or raise "
        "LLM_TIMEOUT if the link is simply slow."
    ),
    KIND_NETWORK: (
        "dashscope.aliyuncs.com is unreachable: check connectivity, DNS, proxy or firewall "
        "settings for this host."
    ),
    KIND_SERVER: (
        "DashScope returned a server-side error: this is usually transient, retry shortly."
    ),
    KIND_PAYLOAD: (
        "The request or the response shape is wrong: check DASHSCOPE_URL and QWEN_MODEL, and "
        "note that this project targets the DashScope text-generation endpoint."
    ),
    KIND_UNKNOWN: "Unexpected failure; see the backend log for the full exception.",
}

# DashScope business error codes seen on an HTTP 200 envelope or on an error status.
_CODE_KIND_RULES: Tuple[Tuple[str, str], ...] = (
    ("invalidapikey", KIND_AUTH),
    ("invalid_api_key", KIND_AUTH),
    ("unauthorized", KIND_AUTH),
    ("arrearage", KIND_AUTH),
    ("overdue", KIND_AUTH),
    ("accessdenied", KIND_AUTH),
    ("throttl", KIND_RATE_LIMIT),
    ("ratelimit", KIND_RATE_LIMIT),
    ("quota", KIND_RATE_LIMIT),
    ("limit", KIND_RATE_LIMIT),
    ("modelnotfound", KIND_PAYLOAD),
    ("invalidparameter", KIND_PAYLOAD),
    ("dataformat", KIND_PAYLOAD),
)


@dataclass
class LLMFailure:
    """A classified live-call failure."""

    kind: str
    message: str
    status_code: Optional[int] = None
    retryable: bool = False
    suggestion: str = ""

    def __post_init__(self) -> None:
        if not self.suggestion:
            self.suggestion = SUGGESTIONS.get(self.kind, SUGGESTIONS[KIND_UNKNOWN])


@dataclass
class LLMProbeResult:
    """Outcome of one real connectivity probe against the configured Qwen endpoint."""

    ok: bool
    kind: str
    message: str
    model: str = ""
    endpoint: str = ""
    api_key_masked: str = ""
    latency_ms: Optional[float] = None
    status_code: Optional[int] = None
    retryable: bool = False
    suggestion: str = ""
    details: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_failure(cls, failure: LLMFailure, **overrides: Any) -> "LLMProbeResult":
        payload: Dict[str, Any] = {
            "ok": False,
            "kind": failure.kind,
            "message": failure.message,
            "status_code": failure.status_code,
            "retryable": failure.retryable,
            "suggestion": failure.suggestion,
        }
        payload.update(overrides)
        return cls(**payload)


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------
def mask_secret(value: Optional[str]) -> str:
    """Render a secret as `sk-abc***wxyz(len=35)` so logs and responses never leak it."""
    if not value:
        return "(not configured)"
    if len(value) <= 10:
        return f"***(len={len(value)})"
    return f"{value[:6]}***{value[-4:]}(len={len(value)})"


def truncate_safely(text: Optional[str], limit: int = 120, ellipsis: str = "…") -> str:
    """
    Trim generated text to `limit` characters without cutting a Latin word in half.

    CJK text has no spaces, so it is cut exactly at the limit; Latin text is cut on the last
    word boundary when that does not discard too much of the budget. Whitespace is collapsed
    first so a stray newline cannot break the frontend layout.
    """
    if text is None:
        return ""
    collapsed = " ".join(str(text).split())
    if limit <= 0:
        return ""
    if len(collapsed) <= limit:
        return collapsed

    window = collapsed[:limit]
    if " " in window:
        head = window.rsplit(" ", 1)[0].rstrip(" ,;:.-")
        if len(head) >= int(limit * 0.6):
            window = head
    return window.rstrip() + ellipsis


def _body_snippet(body: Any, limit: int = 200) -> str:
    """One-line, length-bounded rendering of a response body for logs and reports."""
    if body is None:
        return ""
    if not isinstance(body, str):
        try:
            import json

            body = json.dumps(body, ensure_ascii=False)
        except Exception:  # pragma: no cover - defensive
            body = str(body)
    return " ".join(body.split())[:limit]


def kind_from_dashscope_code(code: Optional[str]) -> Optional[str]:
    """Map a DashScope business error code (e.g. `InvalidApiKey`) to a failure kind."""
    if not code:
        return None
    lowered = str(code).strip().lower()
    for needle, kind in _CODE_KIND_RULES:
        if needle in lowered:
            return kind
    return None


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------
def classify_llm_failure(
    status_code: Optional[int] = None,
    body: Any = "",
    exc: Optional[BaseException] = None,
    code: Optional[str] = None,
) -> LLMFailure:
    """
    Classify a live-call failure into a stable kind with an actionable suggestion.

    Accepts an HTTP status, an optional DashScope business error code, a response body and/or
    the raised exception, so both the timeout path in `diagnostic_service` and the HTTP status
    path in the health probe can share one classifier.
    """
    snippet = _body_snippet(body)

    if exc is not None:
        if isinstance(exc, httpx.TimeoutException):
            return LLMFailure(
                kind=KIND_TIMEOUT,
                message=f"Live call timed out ({exc.__class__.__name__}): {exc}",
                status_code=status_code,
                retryable=True,
            )
        if isinstance(exc, httpx.HTTPError):
            return LLMFailure(
                kind=KIND_NETWORK,
                message=f"Network/transport error ({exc.__class__.__name__}): {exc}",
                status_code=status_code,
                retryable=True,
            )
        return LLMFailure(
            kind=KIND_UNKNOWN,
            message=f"Unexpected error ({exc.__class__.__name__}): {exc}",
            status_code=status_code,
        )

    code_kind = kind_from_dashscope_code(code)
    if code_kind:
        return LLMFailure(
            kind=code_kind,
            message=f"DashScope error code '{code}'" + (f": {snippet}" if snippet else ""),
            status_code=status_code,
            retryable=code_kind in RETRYABLE_KINDS,
        )

    if status_code is None:
        return LLMFailure(kind=KIND_UNKNOWN, message=f"Unclassifiable failure: {snippet}")

    if status_code in (401, 403):
        kind = KIND_AUTH
    elif status_code == 429:
        kind = KIND_RATE_LIMIT
    elif status_code == 404:
        kind = KIND_PAYLOAD
    elif status_code >= 500:
        kind = KIND_SERVER
    elif 400 <= status_code < 500:
        kind = KIND_PAYLOAD
    else:
        kind = KIND_UNKNOWN

    return LLMFailure(
        kind=kind,
        message=f"HTTP {status_code}" + (f": {snippet}" if snippet else ""),
        status_code=status_code,
        retryable=kind in RETRYABLE_KINDS,
    )


# ---------------------------------------------------------------------------
# Connectivity probe
# ---------------------------------------------------------------------------
def _extract_content_and_code(payload: Any) -> Tuple[Optional[str], Optional[str]]:
    """Pull the generated text (and any business error code) out of a DashScope response body."""
    if not isinstance(payload, dict):
        return None, None

    error_code = payload.get("code") or payload.get("error_code")
    error = payload.get("error")
    if isinstance(error, dict):
        error_code = error_code or error.get("code")

    output = payload.get("output")
    content: Optional[str] = None
    if isinstance(output, dict):
        choices = output.get("choices") or []
        if choices and isinstance(choices[0], dict):
            message = choices[0].get("message")
            if isinstance(message, dict):
                content = message.get("content")
            content = content or choices[0].get("text")
        content = content or output.get("text")
    if not content:
        # OpenAI-compatible envelope, in case DASHSCOPE_URL is pointed at compatible-mode.
        choices = payload.get("choices") or []
        if choices and isinstance(choices[0], dict):
            message = choices[0].get("message")
            if isinstance(message, dict):
                content = message.get("content")

    text = content.strip() if isinstance(content, str) else None
    return (text or None), (str(error_code) if error_code else None)


async def probe_llm_connectivity(timeout: Optional[float] = None) -> LLMProbeResult:
    """
    Send one minimal real request to the configured DashScope endpoint.

    Returns a structured `LLMProbeResult`; it never raises, so it is safe to call from a
    request handler. `kind == "ok"` means the key is present, accepted and answered.
    """
    common: Dict[str, Any] = {
        "model": settings.QWEN_MODEL,
        "endpoint": settings.DASHSCOPE_URL,
        "api_key_masked": mask_secret(settings.QWEN_API_KEY),
    }

    if not settings.has_api_key:
        failure = LLMFailure(
            kind=KIND_NO_KEY,
            message=(
                "No QWEN_API_KEY / DASHSCOPE_API_KEY configured; the service is running on the "
                "offline local-knowledge fallback (a valid degraded mode)."
            ),
        )
        return LLMProbeResult.from_failure(failure, **common)

    headers = {
        "Authorization": f"Bearer {settings.QWEN_API_KEY.strip()}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.QWEN_MODEL,
        "input": {
            "messages": [
                {"role": "system", "content": "You are a connectivity test assistant."},
                {"role": "user", "content": "Reply with the single word: OK"},
            ]
        },
        "parameters": {"result_format": "message", "max_tokens": 8, "temperature": 0.0},
    }

    effective_timeout = timeout if timeout is not None else settings.LLM_TIMEOUT
    started = time.perf_counter()
    try:
        async with httpx.AsyncClient(timeout=effective_timeout) as client:
            response = await client.post(settings.DASHSCOPE_URL, json=payload, headers=headers)
    except Exception as exc:  # noqa: BLE001 - the whole point is to never propagate
        failure = classify_llm_failure(exc=exc)
        logger.warning("[llm_diagnostics] connectivity probe failed (%s): %s", failure.kind, failure.message)
        return LLMProbeResult.from_failure(
            failure,
            latency_ms=round((time.perf_counter() - started) * 1000, 1),
            **common,
        )

    latency_ms = round((time.perf_counter() - started) * 1000, 1)

    try:
        body = response.json()
    except Exception:
        body = response.text

    content, error_code = _extract_content_and_code(body)

    if response.status_code == 200 and content and not error_code:
        return LLMProbeResult(
            ok=True,
            kind=KIND_OK,
            message=f"Key accepted and model '{settings.QWEN_MODEL}' responded in {latency_ms} ms.",
            latency_ms=latency_ms,
            status_code=200,
            suggestion=SUGGESTIONS[KIND_OK],
            details={"sample": truncate_safely(content, 60)},
            **common,
        )

    failure = classify_llm_failure(
        status_code=None if response.status_code == 200 else response.status_code,
        body=body,
        code=error_code,
    )
    if response.status_code == 200 and failure.kind == KIND_UNKNOWN:
        failure = LLMFailure(
            kind=KIND_PAYLOAD,
            message="HTTP 200 but the response carried no generated content.",
            status_code=200,
        )
    logger.warning("[llm_diagnostics] connectivity probe failed (%s): %s", failure.kind, failure.message)
    return LLMProbeResult.from_failure(
        failure, latency_ms=latency_ms, status_code=response.status_code, **common
    )

"""
One-command Qwen API key health check.

Answers the question "is my API key actually working?" without starting a server and without
guessing, by sending a single minimal request to the configured DashScope endpoint and
classifying the outcome (missing key / rejected key / rate limit / timeout / network / server).

Usage (from the repository root):

    python -m backend.scripts.check_qwen_key
    python backend/scripts/check_qwen_key.py        # same thing, direct invocation

Exit codes:
    0 - the key is present and the live call succeeded
    1 - the key is missing or the live call failed (the service still works offline)
    2 - the script itself could not run
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.config import settings  # noqa: E402
from backend.app.services.llm_diagnostics import (  # noqa: E402
    KIND_NO_KEY,
    KIND_OK,
    mask_secret,
    probe_llm_connectivity,
)

RULE = "=" * 74


def main() -> int:
    try:
        result = asyncio.run(probe_llm_connectivity())
    except Exception as exc:  # pragma: no cover - defensive, the probe itself never raises
        print(f"could not run the connectivity probe: {exc.__class__.__name__}: {exc}")
        return 2

    print(RULE)
    print("Qwen API key health check")
    print(RULE)
    print(f"  Key detected        : {mask_secret(settings.QWEN_API_KEY)}")
    print("  Source variables    : QWEN_API_KEY / DASHSCOPE_API_KEY (the former wins)")
    print(f"  Model / endpoint    : {settings.QWEN_MODEL} @ {settings.DASHSCOPE_URL}")
    print(f"  Timeout             : {settings.LLM_TIMEOUT}s")
    print("-" * 74)
    print(f"  Probe result        : {'OK' if result.ok else 'FAILED'} ({result.kind})")
    print(f"  Message             : {result.message}")
    if result.latency_ms is not None:
        print(f"  Round trip          : {result.latency_ms} ms")
    if result.suggestion:
        print(f"  Suggested action    : {result.suggestion}")
    print(RULE)

    if result.ok:
        print("Conclusion: the key works, so /api/diagnose will use the live Qwen call path.")
        return 0

    if result.kind == KIND_NO_KEY:
        print("Conclusion: no key configured. The service still answers every request from the")
        print("            offline local-knowledge fallback; set QWEN_API_KEY in .env to go live.")
    else:
        print("Conclusion: the live call path is currently unusable, but the service degrades")
        print("            gracefully - /api/diagnose keeps returning HTTP 200 with")
        print("            fallback_mode=true. Fix the issue above before the demo.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

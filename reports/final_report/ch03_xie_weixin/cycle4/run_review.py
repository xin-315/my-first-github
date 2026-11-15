"""Reproduce the bounded Cycle 4 review without external model calls.

Run from the repository root. Outputs are observations, not acceptance sign-off.
"""
from collections import Counter
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
import logging
import math
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import time
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from backend.app.config import settings

# Force local operation even if a caller has configured credentials.
settings.QWEN_API_KEY = ""
logging.disable(logging.CRITICAL)
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.data.seed_questions import SEED_QUESTIONS
from backend.app.services.diagnostic_service import diagnostic_service
from backend.app.services.question_parser import parse_question_pack_file

OUT = Path(__file__).resolve().parent / "evidence"
OUT.mkdir(exist_ok=True)


def run():
    results = {
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "packages": {name: version(name) for name in ["fastapi", "starlette", "pydantic", "httpx", "pytest"]},
        "scope": "In-process local API and parser checks; no browser, live model or physical network isolation.",
        "bank": {
            "questions": len(SEED_QUESTIONS),
            "subjects": dict(sorted(Counter(q.subject for q in SEED_QUESTIONS).items())),
            "traps": sum(len(q.traps) for q in SEED_QUESTIONS),
        },
        "routes": [{"path": path, "methods": sorted(method.upper() for method in operations
                   if method in {"get", "post", "put", "patch", "delete", "options", "head"})}
                   for path, operations in app.openapi()["paths"].items() if path.startswith("/api")],
    }
    with TestClient(app) as client:
        results["static_root_status"] = client.get("/").status_code
        all_items = client.get("/api/quiz").json()
        results["quiz"] = {
            "all_count": len(all_items),
            "subject_law_count": len(client.get("/api/quiz?subject=law").json()),
            "category_law_count": len(client.get("/api/quiz?category=law").json()),
            "unknown_subject_count": len(client.get("/api/quiz?subject=no-such-subject").json()),
            "public_answer_fields": sorted(set(all_items[0]) & {"answer", "explanation", "traps"}),
            "public_option_fields": sorted(set(all_items[0]["options"][0]) & {"is_correct", "isCorrect", "trap_id", "trapId"}),
        }
        rows = []
        for q in sorted(SEED_QUESTIONS, key=lambda q: q.id):
            for option in q.options:
                response = client.post("/api/diagnose", json={"question_id": q.id, "selected_option": option.key})
                data = response.json()
                correct = option.key == q.answer
                passed = response.status_code == 200 and data.get("is_correct") == correct
                if not correct:
                    trap = q.traps.get(option.trap_id)
                    passed = passed and bool(trap) and data.get("trap_id") == option.trap_id
                    passed = passed and data.get("misconception") == trap.desc and data.get("prerequisite") == trap.prereq
                    passed = passed and data.get("fallback_mode") is True and bool(data.get("socratic_guidance"))
                rows.append({"question_id": q.id, "option": option.key, "status": response.status_code,
                             "expected_correct": correct, "actual_correct": data.get("is_correct"),
                             "expected_trap": option.trap_id, "actual_trap": data.get("trap_id"), "passed": bool(passed)})
        results["option_checks"] = {"total": len(rows), "passed": sum(r["passed"] for r in rows), "rows": rows}
        results["boundary_checks"] = []
        for label, payload in [
            ("unknown_question", {"question_id": "review-missing", "selected_option": "A"}),
            ("unknown_option", {"question_id": "law_1", "selected_option": "E"}),
            ("empty_object", {}),
            ("lowercase_option", {"question_id": "law_1", "selected_option": "a"}),
        ]:
            response = client.post("/api/diagnose", json=payload)
            data = response.json()
            results["boundary_checks"].append({"case": label, "input": payload, "status": response.status_code,
                "selected_key": data.get("selected_key"), "trap_id": data.get("trap_id"),
                "correct_key": data.get("correct_key"), "model_used": data.get("model_used")})
        def summary():
            data = client.get("/api/reports/summary").json()
            return {k: v for k, v in data.items() if k not in {"generated_at", "generatedAt"}}
        before = summary()
        for _ in range(3):
            client.post("/api/diagnose", json={"question_id": "law_1", "selected_option": "A"})
        after = summary()
        results["telemetry"] = {"before": before, "after": after, "unchanged_after_three_attempts": before == after,
                                 "reset_status": client.post("/api/reports/reset").status_code}
        payload = {"question_id": "law_1", "selected_option": "A", "include_socratic": False}
        for _ in range(10):
            client.post("/api/diagnose", json=payload)
        samples = []
        for _ in range(100):
            start = time.perf_counter_ns()
            client.post("/api/diagnose", json=payload)
            samples.append((time.perf_counter_ns() - start) / 1_000_000)
        results["timing"] = {"method": "TestClient in-process round trip; 10 warmups, 100 serial law_1:A calls; no LLM",
            "median_ms": statistics.median(samples), "p95_ms": sorted(samples)[math.ceil(.95 * len(samples))-1],
            "raw_ms": samples, "limit": "Not TCP latency, server startup time, load capacity or a general performance guarantee."}
        mock = AsyncMock(return_value="Synthetic provider response for call-path verification.")
        with patch.object(settings, "QWEN_API_KEY", "synthetic-review-key"), patch.object(diagnostic_service, "_call_dashscope_qwen", mock):
            response = client.post("/api/diagnose", json={"question_id": "law_1", "selected_option": "A", "include_socratic": True})
        results["optional_llm_path"] = {"mock_call_count": mock.await_count, "http_status": response.status_code,
            "fallback_mode": response.json().get("fallback_mode"), "live_network_used": False}
    sample_root = ROOT / "reports/final_report/ch05_dong_siqin/cycle4/samples"
    results["parser"] = {}
    for name in ["valid_pack.json", "invalid_pack.json"]:
        path = sample_root / name
        parsed = parse_question_pack_file(path)
        proc = subprocess.run([sys.executable, str(ROOT / "scripts/validate_question_pack.py"), str(path), "--json"],
                              capture_output=True, text=True, cwd=ROOT)
        results["parser"][name] = {"ok": parsed.ok, "accepted_questions": len(parsed.questions),
            "errors": len(parsed.errors), "warnings": len(parsed.warnings), "codes": parsed.codes(), "cli_exit": proc.returncode,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    audit_path = ROOT / "scripts/audit_hallucination_l1_l3.py"
    audit = audit_path.read_text(encoding="utf-8")
    results["audit_method"] = {
        "fixed_true_verdict_literal": '"human_verdict": "TRUE"' in audit,
        "fixed_consistent_verdict_literal": '"human_verdict": "CONSISTENT"' in audit,
        "interpretation": "Generated human-verdict columns do not establish independent human review.",
    }
    (OUT / "review_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"options": results["option_checks"]["total"], "passed": results["option_checks"]["passed"],
                      "bank": results["bank"], "parser": results["parser"], "timing": {k:v for k,v in results["timing"].items() if k != "raw_ms"}}, indent=2))
    return 0 if all(r["passed"] for r in rows) else 1


if __name__ == "__main__":
    raise SystemExit(run())

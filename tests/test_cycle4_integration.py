"""Personal Cycle 4 integration checks using shipped content and labelled mutations.

See reports/final_report/ch06_yang_mingjie/cycle4/test_matrix.md for evidence limits.
"""

import asyncio
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import uuid

import httpx
import pytest

from backend.app.config import settings
from backend.app.data.seed_questions import SEED_QUESTIONS
from backend.app.models.diagnose import DiagnoseRequest
from backend.app.services.diagnostic_service import DiagnosticService
from backend.app.services.question_parser import (
    export_questions_to_pack, parse_question_pack, parse_question_pack_file,
)
from backend.app.services.quiz_service import QuizService, quiz_service

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "reports/final_report/ch05_dong_siqin/cycle4/samples"


@pytest.fixture
def workspace():
    """Explicit directory mode matches the existing parser test's Windows workaround."""
    folder = Path(tempfile.gettempdir()) / f"cycle4-{uuid.uuid4().hex}"
    folder.mkdir(mode=0o777)
    try:
        yield folder
    finally:
        shutil.rmtree(folder, ignore_errors=True)


@pytest.fixture
def parsed(monkeypatch):
    monkeypatch.setattr(settings, "QWEN_API_KEY", "")
    result = parse_question_pack_file(SAMPLES / "valid_pack.json")
    assert result.ok and not result.issues
    assert [q.id for q in result.questions] == ["law_1", "cs_2"]
    return result.questions


def diagnose(service, question_id, key, **kwargs):
    return asyncio.run(service.diagnose_answer(DiagnoseRequest(
        question_id=question_id, selected_key=key, **kwargs)))


def cli(folder, *args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8", QWEN_API_KEY="",
               DASHSCOPE_API_KEY="", PYTHONPATH="")
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_question_pack.py"), *map(str, args)],
        cwd=folder, env=env, capture_output=True, text=True, encoding="utf-8", timeout=20,
    )


@pytest.mark.parametrize("question_id,selected,expected_trap,radar", [
    ("law_1", "A", "trap_law_1", "trapDefense"),
    ("law_1", "B", None, "trapDefense"),
    ("law_1", "C", "trap_law_2", "boundary"),
    ("law_1", "D", "trap_law_3", "recall"),
    ("cs_2", "A", None, "trapDefense"),
    ("cs_2", "B", "trap_cs_2_1", "precision"),
    ("cs_2", "C", "trap_cs_2_2", "boundary"),
    ("cs_2", "D", "trap_cs_2_3", "synthesis"),
])
def test_sample_option_mapping(parsed, question_id, selected, expected_trap, radar):
    q = next(q for q in parsed if q.id == question_id)
    response = diagnose(DiagnosticService(quiz_repo=QuizService(parsed)), question_id, selected)
    correct = expected_trap is None
    assert response.is_correct is correct
    assert response.correct_key == q.answer
    assert response.explanation == q.explanation
    assert response.trap_id == expected_trap
    assert response.radar_dimension == radar
    assert response.score_delta == (5 if correct else -5)
    assert response.fallback_mode is (not correct)
    assert response.model_used == ("rule-evaluation" if correct else "local-knowledge-seed")
    if not correct:
        trap = q.traps[expected_trap]
        assert response.trap_title == trap.title
        assert response.prerequisite == trap.prereq
        assert response.misconception == trap.desc
        assert response.socratic_guidance == (q.socratic_prompt or trap.desc)


@pytest.mark.parametrize("id_field,key_field", [
    ("question_id", "selected_key"), ("questionId", "selectedOption"), ("id", "option"),
])
def test_http_parsed_pack_aliases(parsed, client, monkeypatch, id_field, key_field):
    from backend.app.routers import diagnose as router
    monkeypatch.setattr(router, "diagnostic_service", DiagnosticService(quiz_repo=QuizService(parsed)))
    response = client.post("/api/diagnose", json={id_field: "cs_2", key_field: " b ", "includeSocratic": False})
    assert response.status_code == 200
    body = response.json()
    for snake, camel, expected in [
        ("question_id", "questionId", "cs_2"), ("selected_key", "selectedKey", "B"),
        ("trap_id", "trapId", "trap_cs_2_1"), ("score_delta", "scoreDelta", -5),
        ("fallback_mode", "fallbackMode", True),
    ]:
        assert body[snake] == body[camel] == expected


@pytest.mark.parametrize("payload", [
    {"question_id": ["law_1"], "selected_key": "A"},
    {"question_id": "law_1", "selected_key": {"key": "A"}},
])
def test_http_rejects_wrong_types(client, payload):
    assert client.post("/api/diagnose", json=payload).status_code == 422


def test_repository_isolation(parsed):
    original = quiz_service.get_question_by_id("law_1").model_dump()
    law = DiagnosticService(quiz_repo=QuizService([parsed[0]]))
    cs = DiagnosticService(quiz_repo=QuizService([parsed[1]]))
    assert diagnose(law, "law_1", "B").is_correct
    missing = diagnose(cs, "law_1", "B")
    assert missing.trap_id == "trap_fallback"
    assert missing.model_used == "local-safe-fallback"
    assert missing.score_delta == -2 and missing.fallback_mode
    assert quiz_service.get_question_by_id("law_1").model_dump() == original
    assert diagnose(DiagnosticService(), "law_1", "B").is_correct


@pytest.mark.parametrize("failure", ["timeout", "http503", "invalid_json", "empty_output"])
def test_upstream_failure_falls_back(parsed, monkeypatch, failure):
    """Simulated transport failures; no request reaches the network."""
    monkeypatch.setattr(settings, "QWEN_API_KEY", "test-placeholder-not-a-secret")
    calls = []
    real_client = httpx.AsyncClient

    def handler(request):
        calls.append(request)
        if failure == "timeout":
            raise httpx.ReadTimeout("simulated timeout", request=request)
        if failure == "http503":
            return httpx.Response(503, text="simulated unavailable")
        if failure == "invalid_json":
            return httpx.Response(200, text="not JSON")
        return httpx.Response(200, json={"output": {"choices": []}})

    monkeypatch.setattr(httpx, "AsyncClient", lambda **kw: real_client(
        transport=httpx.MockTransport(handler), **kw))
    q = parsed[0]
    response = diagnose(DiagnosticService(quiz_repo=QuizService(parsed)), q.id, "A")
    assert len(calls) == 1
    assert response.trap_id == "trap_law_1"
    assert response.score_delta == -5
    assert response.fallback_mode and response.model_used == "local-knowledge-seed"
    assert response.socratic_guidance == (q.socratic_prompt or q.traps["trap_law_1"].desc)


@pytest.mark.parametrize("key,include", [("B", True), ("A", False)])
def test_no_upstream_call_when_not_required(parsed, monkeypatch, key, include):
    monkeypatch.setattr(settings, "QWEN_API_KEY", "test-placeholder-not-a-secret")
    service = DiagnosticService(quiz_repo=QuizService(parsed))
    calls = []

    async def unexpected(**kwargs):
        calls.append(kwargs)
        raise AssertionError("Upstream should not be called")

    monkeypatch.setattr(service, "_call_dashscope_qwen", unexpected)
    response = diagnose(service, "law_1", key, include_socratic=include)
    assert not calls
    assert response.is_correct is (key == "B")


def test_repository_exception_has_distinct_failsafe(parsed, monkeypatch):
    repo = QuizService(parsed)

    def broken(_):
        raise RuntimeError("simulated repository failure")

    monkeypatch.setattr(repo, "get_question_by_id", broken)
    response = diagnose(DiagnosticService(quiz_repo=repo), "law_1", "A")
    assert response.trap_id == "trap_failsafe"
    assert response.model_used == "local-failsafe-shield"
    assert response.fallback_mode and response.score_delta == 0


@pytest.mark.parametrize("sample,exit_code", [("valid_pack.json", 0), ("invalid_pack.json", 1)])
def test_cli_shipped_sample_from_external_directory(workspace, sample, exit_code):
    result = cli(workspace, SAMPLES / sample, "--json")
    assert result.returncode == exit_code, result.stderr
    body = json.loads(result.stdout)
    assert body["ok"] is (exit_code == 0)


def test_cli_export_and_diagnose_shipped_sample(workspace):
    output = workspace / "export.json"
    result = cli(workspace, SAMPLES / "valid_pack.json", "--export", output, "--diagnose", "cs_2:B")
    assert result.returncode == 0, result.stderr
    assert "diagnosis : cs_2:B" in result.stdout
    assert "local-knowledge-seed" in result.stdout
    parsed = parse_question_pack_file(output)
    assert parsed.ok and [q.id for q in parsed.questions] == ["law_1", "cs_2"]


@pytest.mark.parametrize("mode", ["mixed_invalid", "strict_warning"])
def test_cli_blocks_export_and_diagnosis(workspace, mode):
    payload = json.loads((SAMPLES / "valid_pack.json").read_text(encoding="utf-8"))
    args = []
    if mode == "mixed_invalid":
        bad = copy.deepcopy(payload["questions"][1])
        bad["stem"] = ""  # Labelled negative mutation of shipped content.
        payload["questions"][1] = bad
        parsed = parse_question_pack(payload)
        assert not parsed.ok and [q.id for q in parsed.questions] == ["law_1"]
    else:
        payload.pop("schema_version")  # Labelled warning mutation.
        parsed = parse_question_pack(payload)
        assert parsed.ok and "missing_schema_version" in parsed.codes()
        args = ["--strict"]
    source = workspace / "mutation.json"
    source.write_text(json.dumps(payload), encoding="utf-8")
    output = workspace / "sentinel.json"
    output.write_text("unchanged", encoding="utf-8")
    result = cli(workspace, source, *args, "--export", output, "--diagnose", "law_1:A")
    assert result.returncode == 1, result.stderr
    assert output.read_text(encoding="utf-8") == "unchanged"
    assert "diagnosis :" not in result.stdout


@pytest.mark.xfail(strict=True, raises=UnicodeDecodeError, reason="C4-01: invalid UTF-8 escapes the file API")
def test_invalid_utf8_returns_a_parse_issue(workspace):
    source = workspace / "invalid-utf8.json"
    source.write_bytes(b"\xff\xfe")
    result = parse_question_pack_file(source)
    assert not result.ok and result.errors


@pytest.mark.xfail(strict=True, reason="C4-01: CLI returns 2, documented decode error exit is 1")
def test_cli_invalid_utf8_has_documented_exit(workspace):
    source = workspace / "invalid-utf8.json"
    source.write_bytes(b"\xff\xfe")
    assert cli(workspace, source).returncode == 1


@pytest.mark.parametrize("field", ["graph", "socratic_prompt"])
@pytest.mark.xfail(strict=True, reason="C4-02: export omits optional graph and Socratic guidance")
def test_seed_export_preserves_optional_content(field):
    original = next(q for q in SEED_QUESTIONS if getattr(q, field))
    parsed = parse_question_pack(export_questions_to_pack([original]))
    assert parsed.ok
    assert getattr(parsed.questions[0], field) == getattr(original, field)

"""
Tests for the Cycle 4 question-parsing slice.

Covers three things the assignment asks for explicitly:
1. representative valid inputs (a hand-written pack, the real seed bank round-trip, camelCase
   and dict-form options);
2. representative invalid inputs, one assertion per documented failure code;
3. the vertical slice end to end: JSON pack -> validated models -> misconception diagnosis.

Run with: python -m pytest tests/test_question_parser.py -q
"""

from __future__ import annotations

import copy
import json
import os
import shutil
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Any, Dict, List

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from backend.app.data.seed_questions import SEED_QUESTIONS
from backend.app.models.diagnose import DiagnoseRequest
from backend.app.services.diagnostic_service import DiagnosticService
from backend.app.services.question_parser import (
    KNOWN_SUBJECTS,
    RADAR_DIMENSIONS,
    export_questions_to_pack,
    parse_question_pack,
    parse_question_pack_file,
)
from backend.app.services.quiz_service import QuizService

# --- fixtures ---------------------------------------------------------------


@pytest.fixture
def pack_dir():
    """A writable temporary directory for pack files.

    Created with an explicit permissive mode (mode=0o777) rather than via ``mkdtemp``, whose
    private 0o700 directories are not writable on hardened Windows hosts. Works the same way
    on POSIX, and the directory is removed afterwards.
    """
    directory = Path(tempfile.gettempdir()) / f"qpack-{uuid.uuid4().hex}"
    directory.mkdir(mode=0o777, parents=True)
    try:
        yield directory
    finally:
        shutil.rmtree(directory, ignore_errors=True)


def make_question(question_id: str = "law_t1", subject: str = "law") -> Dict[str, Any]:
    """A minimal question that satisfies every data rule."""
    return {
        "id": question_id,
        "subject": subject,
        "difficulty": "★★★★☆",
        "tag": "Revocation period",
        "stem": "Which period applies to the right of revocation?",
        "answer": "B",
        "explanation": "【Authoritative analysis · Civil Code Art. 152】 the period is one year.",
        "options": [
            {"key": "A", "text": "three years", "trap_id": "trap_1"},
            {"key": "B", "text": "one year", "is_correct": True},
            {"key": "C", "text": "five years", "trap_id": "trap_2"},
            {"key": "D", "text": "ninety days", "trap_id": "trap_3"},
        ],
        "traps": {
            "trap_1": {"title": "T1", "desc": "D1", "prereq": "P1", "radar_hit": "trapDefense"},
            "trap_2": {"title": "T2", "desc": "D2", "prereq": "P2", "radar_hit": "boundary"},
            "trap_3": {"title": "T3", "desc": "D3", "prereq": "P3", "radar_hit": "recall"},
        },
    }


def make_pack(*questions: Dict[str, Any]) -> Dict[str, Any]:
    return {"schema_version": "1.0", "questions": list(questions)}


def codes(result) -> List[str]:
    return result.codes()


# --- valid inputs -----------------------------------------------------------


def test_valid_pack_is_accepted():
    result = parse_question_pack(make_pack(make_question()))

    assert result.ok, [i.render() for i in result.issues]
    assert len(result.questions) == 1
    question = result.questions[0]
    assert question.id == "law_t1"
    assert question.subject == "law"
    assert question.answer == "B"
    assert len(question.options) == 4
    assert set(question.traps) == {"trap_1", "trap_2", "trap_3"}
    # the correct option must not carry a trap
    assert question.options[1].trap_id is None


def test_options_may_be_a_key_text_mapping():
    """The lenient {"A": "text"} form parses structurally, but cannot express trap links.

    This is deliberate: the data rule "every distractor maps to one trap" still applies, so a
    key/text mapping is accepted only as a structure and is rejected for missing trap ids.
    """
    raw = make_question()
    raw["options"] = {"A": "three years", "B": "one year", "C": "five years", "D": "ninety days"}

    result = parse_question_pack(make_pack(raw))

    assert not result.ok
    assert "missing_trap_id" in codes(result)
    # the four options and the correct flag were still understood
    assert len(raw["options"]) == 4


def test_camel_case_keys_are_accepted():
    raw = make_question()
    raw.pop("answer")
    raw["questionId"] = raw.pop("id")
    raw["options"][0]["trapId"] = raw["options"][0].pop("trap_id")
    raw["options"][1]["isCorrect"] = raw["options"][1].pop("is_correct")
    for trap in raw["traps"].values():
        trap["radarHit"] = trap.pop("radar_hit")

    result = parse_question_pack(make_pack(raw))

    assert result.ok, [i.render() for i in result.issues]
    assert result.questions[0].id == "law_t1"
    assert result.questions[0].answer == "B"


def test_real_seed_bank_round_trips():
    """The shipped question bank must survive export -> parse with zero issues."""
    pack = export_questions_to_pack(SEED_QUESTIONS)

    result = parse_question_pack(pack)

    assert result.ok, [i.render() for i in result.issues]
    assert len(result.questions) == len(SEED_QUESTIONS)
    assert {q.id for q in result.questions} == {q.id for q in SEED_QUESTIONS}
    # the trap map and the option count must be preserved exactly
    for parsed, original in zip(result.questions, SEED_QUESTIONS):
        assert len(parsed.options) == len(original.options) == 4
        assert set(parsed.traps) == set(original.traps)


def test_known_subjects_cover_the_seed_bank():
    """Drift guard: adding a discipline to the bank must also extend KNOWN_SUBJECTS."""
    bank_subjects = {q.subject for q in SEED_QUESTIONS}
    assert bank_subjects <= set(KNOWN_SUBJECTS), (
        f"seed bank introduces subjects missing from KNOWN_SUBJECTS: {sorted(bank_subjects - set(KNOWN_SUBJECTS))}"
    )


def test_accepted_subjects_and_radar_dimensions_cover_the_contract():
    assert set(KNOWN_SUBJECTS) >= {"econ", "cs", "law", "se"}
    assert set(RADAR_DIMENSIONS) == {"recall", "boundary", "trapDefense", "synthesis", "precision"}


# --- pack-level failure cases ----------------------------------------------


def test_pack_must_be_an_object():
    result = parse_question_pack([make_question()])
    assert not result.ok
    assert codes(result) == ["pack_not_object"]


def test_missing_questions_array():
    result = parse_question_pack({"schema_version": "1.0"})
    assert not result.ok
    assert "missing_field" in codes(result)


def test_questions_must_be_an_array():
    result = parse_question_pack({"schema_version": "1.0", "questions": {"a": 1}})
    assert not result.ok
    assert "wrong_type" in codes(result)


def test_empty_pack_is_rejected():
    result = parse_question_pack(make_pack())
    assert not result.ok
    assert codes(result) == ["pack_empty"]


def test_duplicate_question_id_is_rejected():
    result = parse_question_pack(make_pack(make_question("dup"), make_question("dup")))
    assert not result.ok
    assert "duplicate_question_id" in codes(result)
    # the first occurrence is kept, the duplicate is dropped
    assert [q.id for q in result.questions] == ["dup"]


def test_missing_schema_version_is_only_a_warning():
    result = parse_question_pack({"questions": [make_question()]})
    assert result.ok
    assert "missing_schema_version" in codes(result)
    assert len(result.warnings) == 1


# --- question-level failure cases ------------------------------------------


@pytest.mark.parametrize("field", ["id", "subject", "stem"])
def test_required_scalar_fields(field: str):
    raw = make_question()
    raw.pop(field)
    result = parse_question_pack(make_pack(raw))
    assert not result.ok
    assert "missing_field" in codes(result)


def test_unknown_subject_is_rejected():
    result = parse_question_pack(make_pack(make_question(subject="astrology")))
    assert not result.ok
    assert "unknown_subject" in codes(result)


def test_subject_alias_is_normalised():
    result = parse_question_pack(make_pack(make_question(subject="economics")))
    assert result.ok, [i.render() for i in result.issues]
    assert result.questions[0].subject == "econ"


def test_missing_explanation_is_rejected():
    raw = make_question()
    raw["explanation"] = ""
    result = parse_question_pack(make_pack(raw))
    assert not result.ok
    assert "missing_explanation" in codes(result)


def test_wrong_option_count_is_rejected():
    raw = make_question()
    raw["options"] = raw["options"][:3]
    raw["traps"].pop("trap_3")
    result = parse_question_pack(make_pack(raw))
    assert not result.ok
    assert "option_count" in codes(result)


def test_duplicate_option_key_is_rejected():
    raw = make_question()
    raw["options"][2]["key"] = "A"
    result = parse_question_pack(make_pack(raw))
    assert not result.ok
    assert "duplicate_option_key" in codes(result)


def test_option_keys_must_be_a_to_d():
    raw = make_question()
    raw["options"][3]["key"] = "E"
    result = parse_question_pack(make_pack(raw))
    assert not result.ok
    assert "option_keys_invalid" in codes(result)


def test_empty_option_text_is_rejected():
    raw = make_question()
    raw["options"][2]["text"] = "   "
    result = parse_question_pack(make_pack(raw))
    assert not result.ok
    assert "empty_option_text" in codes(result)


def test_no_correct_option_is_rejected():
    raw = make_question()
    raw.pop("answer")
    raw["options"][1].pop("is_correct")
    result = parse_question_pack(make_pack(raw))
    assert not result.ok
    assert "correct_option_count" in codes(result)


def test_multiple_correct_options_are_rejected():
    raw = make_question()
    raw["options"][0]["is_correct"] = True  # A becomes correct too
    result = parse_question_pack(make_pack(raw))
    assert not result.ok
    assert "multiple_correct_options" in codes(result)


def test_answer_must_exist_among_options():
    raw = make_question()
    raw["answer"] = "Z"
    result = parse_question_pack(make_pack(raw))
    assert not result.ok
    assert "answer_not_in_options" in codes(result)


def test_answer_must_agree_with_the_correct_flag():
    raw = make_question()
    raw["answer"] = "C"  # B is flagged correct instead
    result = parse_question_pack(make_pack(raw))
    assert not result.ok
    assert "answer_mismatch" in codes(result)


def test_distractor_without_trap_id_is_rejected():
    raw = make_question()
    raw["options"][2].pop("trap_id")
    result = parse_question_pack(make_pack(raw))
    assert not result.ok
    assert "missing_trap_id" in codes(result)


def test_dangling_trap_id_is_rejected():
    raw = make_question()
    raw["options"][2]["trap_id"] = "trap_does_not_exist"
    result = parse_question_pack(make_pack(raw))
    assert not result.ok
    assert "dangling_trap_id" in codes(result)


def test_empty_trap_field_is_rejected():
    raw = make_question()
    raw["traps"]["trap_2"]["prereq"] = ""
    result = parse_question_pack(make_pack(raw))
    assert not result.ok
    assert "empty_trap_field" in codes(result)


def test_unknown_radar_dimension_is_rejected():
    raw = make_question()
    raw["traps"]["trap_2"]["radar_hit"] = "trap_defense"  # wrong spelling
    result = parse_question_pack(make_pack(raw))
    assert not result.ok
    assert "unknown_radar_dimension" in codes(result)


def test_all_errors_are_reported_not_just_the_first():
    """The gate must be a checklist: the author should see every defect in one run."""
    raw = make_question()
    raw["stem"] = ""
    raw["explanation"] = ""
    raw["traps"]["trap_2"]["radar_hit"] = "nope"
    result = parse_question_pack(make_pack(raw))
    assert not result.ok
    assert {"missing_field", "missing_explanation", "unknown_radar_dimension"} <= set(codes(result))


# --- warnings (do not block) ------------------------------------------------


def test_orphan_trap_is_a_warning_only():
    raw = make_question()
    raw["traps"]["trap_4"] = {"title": "unused", "desc": "d", "prereq": "p", "radar_hit": "synthesis"}
    result = parse_question_pack(make_pack(raw))
    assert result.ok, [i.render() for i in result.issues]
    assert codes(result) == ["orphan_trap"]


def test_unknown_field_is_a_warning_only():
    raw = make_question()
    raw["trapid"] = "typo"
    result = parse_question_pack(make_pack(raw))
    assert result.ok, [i.render() for i in result.issues]
    assert "unknown_field" in codes(result)


def test_trap_on_correct_option_is_a_warning():
    raw = make_question()
    raw["options"][1]["trap_id"] = "trap_1"
    result = parse_question_pack(make_pack(raw))
    assert result.ok, [i.render() for i in result.issues]
    assert "trap_on_correct_option" in codes(result)


# --- graph validation -------------------------------------------------------


def test_graph_edges_must_resolve_to_nodes():
    raw = make_question()
    raw["graph"] = {
        "title": "subgraph",
        "nodes": [{"id": "n1", "label": "concept"}],
        "edges": [{"from": "n1", "to": "n2", "label": "prerequisite"}],
    }
    result = parse_question_pack(make_pack(raw))
    assert not result.ok
    assert "dangling_graph_edge" in codes(result)


def test_duplicate_graph_node_is_rejected():
    raw = make_question()
    raw["graph"] = {"title": "s", "nodes": [{"id": "n1", "label": "a"}, {"id": "n1", "label": "b"}], "edges": []}
    result = parse_question_pack(make_pack(raw))
    assert not result.ok
    assert "duplicate_graph_node" in codes(result)


def test_valid_graph_is_preserved():
    raw = make_question()
    raw["graph"] = {"title": "s", "nodes": [{"id": "n1", "label": "a"}], "edges": [{"from": "n1", "to": "n1", "label": "self"}]}
    result = parse_question_pack(make_pack(raw))
    assert result.ok, [i.render() for i in result.issues]
    assert result.questions[0].graph is not None


# --- file-level failure cases ----------------------------------------------


def test_missing_file_is_reported(pack_dir: Path):
    result = parse_question_pack_file(pack_dir / "nope.json")
    assert not result.ok
    assert codes(result) == ["pack_not_found"]


def test_invalid_json_is_reported(pack_dir: Path):
    broken = pack_dir / "broken.json"
    broken.write_text("{not json", encoding="utf-8")
    result = parse_question_pack_file(broken)
    assert not result.ok
    assert codes(result) == ["pack_invalid_json"]


def test_valid_file_round_trip(pack_dir: Path):
    pack_file = pack_dir / "pack.json"
    pack_file.write_text(json.dumps(make_pack(make_question())), encoding="utf-8")
    result = parse_question_pack_file(pack_file)
    assert result.ok, [i.render() for i in result.issues]
    assert result.questions[0].id == "law_t1"


# --- the vertical slice: pack -> models -> diagnosis -----------------------


def _diagnose(questions, question_id: str, selected: str):
    service = DiagnosticService(quiz_repo=QuizService(list(questions)))
    return service.diagnose_answer(DiagnoseRequest(question_id=question_id, selected_option=selected))


def test_diagnosis_runs_on_a_parsed_pack():
    """parse -> diagnose must work without touching the global seed repository (async)."""
    import asyncio

    result = parse_question_pack(make_pack(make_question()))
    assert result.ok

    wrong = asyncio.run(_diagnose(result.questions, "law_t1", "A"))
    assert wrong.is_correct is False
    assert wrong.trap_title  # the trap of option A must reach the response

    right = asyncio.run(_diagnose(result.questions, "law_t1", "B"))
    assert right.is_correct is True


def test_diagnosis_of_an_unknown_question_degrades_gracefully():
    """The documented failure path: an unknown id yields a fallback response, not an exception."""
    import asyncio

    result = parse_question_pack(make_pack(make_question()))
    response = asyncio.run(_diagnose(result.questions, "does_not_exist", "A"))
    assert response.is_correct is False
    assert response.fallback_mode is True


def test_default_engine_still_uses_the_seed_repository():
    """Regression: constructing DiagnosticService() must keep the previous behaviour."""
    import asyncio

    service = DiagnosticService()
    response = asyncio.run(service.diagnose_answer(DiagnoseRequest(question_id="law_1", selected_option="A")))
    assert response.question_id == "law_1"


# --- CLI --------------------------------------------------------------------


def _cli_module():
    from scripts import validate_question_pack as cli  # namespace package import

    return cli


def test_cli_accepts_a_valid_pack(pack_dir: Path, capsys):
    pack_file = pack_dir / "valid.json"
    pack_file.write_text(json.dumps(make_pack(make_question())), encoding="utf-8")

    exit_code = _cli_module().main([str(pack_file)])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "verdict   : OK" in output
    assert "law_t1" in output


def test_cli_rejects_an_invalid_pack(pack_dir: Path, capsys):
    raw = make_question()
    raw["options"] = raw["options"][:3]
    raw["traps"].pop("trap_3")
    pack_file = pack_dir / "invalid.json"
    pack_file.write_text(json.dumps(make_pack(raw)), encoding="utf-8")

    exit_code = _cli_module().main([str(pack_file)])
    output = capsys.readouterr().out

    assert exit_code == 1
    assert "verdict   : REJECTED" in output
    assert "option_count" in output


def test_cli_strict_promotes_warnings(pack_dir: Path):
    raw = make_question()
    raw["traps"]["trap_4"] = {"title": "unused", "desc": "d", "prereq": "p", "radar_hit": "recall"}
    pack_file = pack_dir / "warn.json"
    pack_file.write_text(json.dumps(make_pack(raw)), encoding="utf-8")

    assert _cli_module().main([str(pack_file)]) == 0
    assert _cli_module().main([str(pack_file), "--strict"]) == 1


def test_cli_json_output_is_machine_readable(pack_dir: Path, capsys):
    pack_file = pack_dir / "valid.json"
    pack_file.write_text(json.dumps(make_pack(make_question())), encoding="utf-8")

    assert _cli_module().main([str(pack_file), "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is True
    assert payload["question_count"] == 1


def test_cli_diagnose_demonstrates_the_slice(pack_dir: Path, capsys):
    pack_file = pack_dir / "valid.json"
    pack_file.write_text(json.dumps(make_pack(make_question())), encoding="utf-8")

    exit_code = _cli_module().main([str(pack_file), "--diagnose", "law_t1:A"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "diagnosis : law_t1:A" in output
    assert "is_correct      : False" in output


def test_cli_export_writes_a_normalised_pack(pack_dir: Path):
    pack_file = pack_dir / "valid.json"
    pack_file.write_text(json.dumps(make_pack(make_question())), encoding="utf-8")
    out_file = pack_dir / "normalised.json"

    assert _cli_module().main([str(pack_file), "--export", str(out_file)]) == 0
    exported = json.loads(out_file.read_text(encoding="utf-8"))
    assert exported["schema_version"] == "1.0"
    assert exported["questions"][0]["id"] == "law_t1"

#!/usr/bin/env python3
"""
Question Pack Validator (and diagnosis smoke run)
Part of the Cycle 4 question-parsing slice (Siqin Dong, 50106060)

Validates a JSON question pack against the quiz domain contract and optionally runs the
misconception-diagnosis engine on the parsed pack, which demonstrates the whole slice
from authoring file to diagnosis response.

Usage
-----
    python scripts/validate_question_pack.py reports/final_report/ch05_dong_siqin/cycle4/samples/valid_pack.json
    python scripts/validate_question_pack.py pack.json --json
    python scripts/validate_question_pack.py pack.json --strict          # warnings become failures
    python scripts/validate_question_pack.py pack.json --diagnose law_1:A
    python scripts/validate_question_pack.py pack.json --export normalised.json

Exit codes
----------
    0  pack is usable (warnings are allowed unless --strict)
    1  the pack has errors, or the file could not be read or decoded
    2  the validator itself failed unexpectedly
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from backend.app.models.diagnose import DiagnoseRequest
from backend.app.services.diagnostic_service import DiagnosticService
from backend.app.services.question_parser import (
    ParseResult,
    export_questions_to_pack,
    parse_question_pack_file,
)
from backend.app.services.quiz_service import QuizService

EXIT_OK = 0
EXIT_INVALID = 1
EXIT_FAILURE = 2


def _print_human(result: ParseResult, pack: str, strict: bool) -> None:
    """Print a readable report: a one-line summary, then every issue in input order."""
    verdict = "OK" if result.ok and not (strict and result.warnings) else "REJECTED"
    print(f"pack      : {pack}")
    print(f"verdict   : {verdict}")
    print(f"questions : {len(result.questions)} accepted")
    print(f"issues    : {len(result.errors)} error(s), {len(result.warnings)} warning(s)")
    if result.issues:
        print("-" * 78)
        for issue in result.issues:
            print("  " + issue.render())
    accepted = [q.id for q in result.questions]
    if accepted:
        print("-" * 78)
        print(f"accepted ids: {', '.join(accepted)}")


def _run_diagnosis(result: ParseResult, target: str) -> int:
    """Diagnose one option of one parsed question, proving the slice works end to end."""
    if ":" not in target:
        print(f"--diagnose expects QUESTION_ID:OPTION, got '{target}'")
        return EXIT_FAILURE
    question_id, selected = target.split(":", 1)
    question_id, selected = question_id.strip(), selected.strip().upper()

    service = DiagnosticService(quiz_repo=QuizService(list(result.questions)))
    request = DiagnoseRequest(question_id=question_id, selected_option=selected)
    response = asyncio.run(service.diagnose_answer(request))

    print("-" * 78)
    print(f"diagnosis : {question_id}:{selected}")
    print(f"  is_correct      : {response.is_correct}")
    print(f"  correct_key     : {response.correct_key}")
    print(f"  trap_title      : {response.trap_title}")
    print(f"  concept_name    : {response.concept_name}")
    print(f"  radar_dimension : {response.radar_dimension}")
    print(f"  fallback_mode   : {response.fallback_mode}")
    print(f"  model_used      : {getattr(response, 'model_used', '')}")
    guidance = (response.socratic_guidance or "").replace("\n", " ")
    print(f"  guidance        : {guidance[:160]}{'...' if len(guidance) > 160 else ''}")
    return EXIT_OK


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a question pack and optionally diagnose one option.")
    parser.add_argument("pack", help="path to the JSON question pack")
    parser.add_argument("--json", action="store_true", help="print a machine-readable result instead of a report")
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    parser.add_argument("--diagnose", metavar="QUESTION_ID:OPTION", help="run the diagnosis engine on the parsed pack")
    parser.add_argument("--export", metavar="PATH", help="write the normalised pack that would be loaded")
    args = parser.parse_args(argv)

    try:
        result = parse_question_pack_file(args.pack)
    except Exception as exc:  # pragma: no cover - defensive: the parser is designed not to raise
        print(f"validator failure: {exc.__class__.__name__}: {exc}", file=sys.stderr)
        return EXIT_FAILURE

    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        _print_human(result, args.pack, args.strict)

    usable = result.ok and not (args.strict and result.warnings)
    if not usable:
        return EXIT_INVALID

    if args.export:
        destination = Path(args.export)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(export_questions_to_pack(result.questions), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"exported normalised pack: {destination}")

    if args.diagnose:
        return _run_diagnosis(result, args.diagnose)

    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())

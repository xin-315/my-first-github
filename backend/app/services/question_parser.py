"""
Question Pack Parser and Validator
==================================

Cycle 4 slice (Siqin Dong, 50106060): turn an authoring file into validated
``QuizItem`` models, or into a structured list of coded issues.

Why this module exists
----------------------
Before this slice, quiz content could only be added by editing
``backend/app/data/seed_questions.py`` by hand. That has three costs: the author must be a
Python developer, a malformed entry is only discovered at request time, and there is no
machine-readable contract for quiz content. This parser is the ingestion gate: it reads a
JSON question pack, checks the data rules that the diagnosis engine relies on, and either
returns typed models or reports every problem it found (not only the first).

It does not replace the diagnosis engine. It guarantees that whatever reaches the engine is
structurally and semantically complete, so a diagnosis can never fail because of bad content.

Authoring format (schema version 1.0)
-------------------------------------
.. code-block:: json

    {
      "schema_version": "1.0",
      "questions": [
        {
          "id": "law_1",
          "subject": "law",
          "difficulty": "★★★★☆",
          "tag": "Revocation period",
          "stem": "...",
          "options": [
            {"key": "A", "text": "...", "trap_id": "trap_law_1"},
            {"key": "B", "text": "...", "is_correct": true}
          ],
          "answer": "B",
          "explanation": "【Authoritative analysis ...】...",
          "traps": {
            "trap_law_1": {"title": "...", "desc": "...", "prereq": "...", "radar_hit": "trapDefense"}
          }
        }
      ]
    }

Both snake_case and camelCase keys are accepted, mirroring the ``CamelModel`` convention used
by the rest of the backend.

Usage
-----
    from backend.app.services.question_parser import parse_question_pack_file

    result = parse_question_pack_file("packs/law.json")
    if not result.ok:
        for issue in result.errors:
            print(issue.render())
    else:
        questions = result.questions
"""

from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from pydantic import ValidationError

from backend.app.models.quiz import QuizItem
from backend.app.services.quiz_service import QuizService

# --- Contract constants ------------------------------------------------------

SCHEMA_VERSION = "1.0"
SUPPORTED_SCHEMA_VERSIONS: Tuple[str, ...] = ("1.0",)

#: Discipline codes present in the curated bank (verified against ``SEED_QUESTIONS`` on
#: 2026-11-03: law, cs, econ and se carry three questions each; or, mis, prob_stat, mkt and
#: eng carry one each). Extend this tuple when a new discipline is authored, and the drift
#: test in ``tests/test_question_parser.py`` will fail until you do.
KNOWN_SUBJECTS: Tuple[str, ...] = (
    "econ",
    "cs",
    "law",
    "se",
    "or",
    "mis",
    "prob_stat",
    "mkt",
    "eng",
)

#: The five radar dimensions defined by the mastery dashboard contract.
RADAR_DIMENSIONS: Tuple[str, ...] = (
    "recall",
    "boundary",
    "trapDefense",
    "synthesis",
    "precision",
)

#: Exactly four options are required by the interface and by the data rules of Chapter 5.3.4.
REQUIRED_OPTION_KEYS: Tuple[str, ...] = ("A", "B", "C", "D")
REQUIRED_OPTION_COUNT = len(REQUIRED_OPTION_KEYS)

SEVERITY_ERROR = "error"
SEVERITY_WARNING = "warning"

_ALLOWED_QUESTION_KEYS = frozenset(
    {
        "id",
        "question_id",
        "questionId",
        "subject",
        "difficulty",
        "tag",
        "stem",
        "options",
        "answer",
        "explanation",
        "trap_hint",
        "trapHint",
        "traps",
        "graph",
        "socratic_prompt",
        "socraticPrompt",
    }
)
_ALLOWED_OPTION_KEYS = frozenset({"key", "text", "is_correct", "isCorrect", "trap_id", "trapId"})
_ALLOWED_TRAP_KEYS = frozenset({"title", "desc", "prereq", "radar_hit", "radarHit"})

# --- Result types ------------------------------------------------------------


class ParseIssue:
    """One problem found while parsing a pack.

    ``path`` is a JSON-path-like locator so the author can find the offending field, and
    ``code`` is a stable identifier that tests and tooling can assert on.
    """

    __slots__ = ("code", "path", "message", "severity")

    def __init__(self, code: str, path: str, message: str, severity: str = SEVERITY_ERROR) -> None:
        self.code = code
        self.path = path
        self.message = message
        self.severity = severity

    def render(self) -> str:
        """Render as one human-readable line for CLI output."""
        return f"[{self.severity}] {self.code} at {self.path}: {self.message}"

    def to_dict(self) -> Dict[str, str]:
        """Serialise for machine-readable output."""
        return {"code": self.code, "path": self.path, "message": self.message, "severity": self.severity}

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"ParseIssue(code={self.code!r}, path={self.path!r}, severity={self.severity!r})"


class ParseResult:
    """Outcome of parsing one pack: the accepted models plus every issue found."""

    __slots__ = ("questions", "issues")

    def __init__(self, questions: List[QuizItem], issues: List[ParseIssue]) -> None:
        self.questions = questions
        self.issues = issues

    @property
    def errors(self) -> List[ParseIssue]:
        return [i for i in self.issues if i.severity == SEVERITY_ERROR]

    @property
    def warnings(self) -> List[ParseIssue]:
        return [i for i in self.issues if i.severity == SEVERITY_WARNING]

    @property
    def ok(self) -> bool:
        """True when the pack can safely be loaded (warnings alone do not block)."""
        return not self.errors

    def codes(self) -> List[str]:
        """Sorted, de-duplicated issue codes, convenient for assertions."""
        return sorted({issue.code for issue in self.issues})

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ok": self.ok,
            "question_count": len(self.questions),
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "issues": [issue.to_dict() for issue in self.issues],
        }


# --- Helpers -----------------------------------------------------------------


def _norm_key(raw: Dict[str, Any], *names: str) -> Any:
    """Return the first present value among ``names`` (snake_case / camelCase tolerance)."""
    for name in names:
        if name in raw:
            return raw[name]
    return None


def _as_text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _issue(issues: List[ParseIssue], code: str, path: str, message: str, severity: str = SEVERITY_ERROR) -> None:
    issues.append(ParseIssue(code=code, path=path, message=message, severity=severity))


def _load_quiz_service(questions: Sequence[QuizItem]) -> QuizService:
    """Build a service over parsed questions, so the diagnosis engine can be exercised offline."""
    return QuizService(list(questions))


# --- Option parsing ----------------------------------------------------------


def _parse_options(
    raw_options: Any,
    answer: Optional[str],
    issues: List[ParseIssue],
    path: str,
) -> Tuple[List[Dict[str, Any]], List[str]]:
    """Normalise options to a list of dicts and report structural problems.

    Returns ``(options, referenced_trap_ids)``. Both ``{"A": "text"}`` and
    ``[{"key": "A", "text": ...}]`` are accepted.
    """
    normalised: List[Dict[str, Any]] = []
    referenced: List[str] = []

    if isinstance(raw_options, dict):
        for key, text in raw_options.items():
            normalised.append({"key": str(key), "text": text})
    elif isinstance(raw_options, list):
        for index, item in enumerate(raw_options):
            item_path = f"{path}[{index}]"
            if not isinstance(item, dict):
                _issue(issues, "wrong_type", item_path, f"option must be an object, got {type(item).__name__}")
                continue
            unknown = set(item) - _ALLOWED_OPTION_KEYS
            for field in sorted(unknown):
                _issue(issues, "unknown_field", f"{item_path}.{field}", f"unknown option field '{field}'", SEVERITY_WARNING)

            key = _as_text(_norm_key(item, "key"))
            text = _as_text(_norm_key(item, "text"))
            if not key:
                _issue(issues, "missing_field", f"{item_path}.key", "option key is required")
            if not text:
                _issue(issues, "empty_option_text", f"{item_path}.text", "option text is empty")

            is_correct = bool(_norm_key(item, "is_correct", "isCorrect"))
            trap_id = _as_text(_norm_key(item, "trap_id", "trapId"))
            if trap_id:
                referenced.append(trap_id)

            normalised.append(
                {
                    "key": key.upper(),
                    "text": text,
                    "is_correct": is_correct,
                    "trap_id": trap_id or None,
                }
            )
    elif raw_options is None:
        _issue(issues, "missing_field", path, "options are required")
    else:
        _issue(issues, "wrong_type", path, f"options must be a list or an object, got {type(raw_options).__name__}")

    # --- count / keys ---
    if normalised and len(normalised) != REQUIRED_OPTION_COUNT:
        _issue(
            issues,
            "option_count",
            path,
            f"expected {REQUIRED_OPTION_COUNT} options, found {len(normalised)}",
        )

    keys = [opt["key"] for opt in normalised if opt.get("key")]
    if any(not key or len(key) != 1 or not key.isalpha() for key in keys):
        _issue(issues, "invalid_option_key", path, f"option keys must be single letters, got {keys}")
    if len(set(keys)) != len(keys):
        _issue(issues, "duplicate_option_key", path, f"duplicate option keys in {keys}")
    if keys and set(keys) != set(REQUIRED_OPTION_KEYS):
        _issue(issues, "option_keys_invalid", path, f"option keys must be exactly A-D, got {sorted(keys)}")

    # --- exactly one correct option ---
    if answer is None:
        # Fall back to the is_correct flags when the pack omits `answer`.
        flag_correct = [opt["key"] for opt in normalised if opt.get("is_correct")]
        if len(flag_correct) != 1:
            _issue(
                issues,
                "correct_option_count",
                path,
                f"expected exactly one correct option, found {len(flag_correct)} ({flag_correct})",
            )
    return normalised, referenced


# --- Trap parsing ------------------------------------------------------------


def _parse_traps(
    raw_traps: Any,
    issues: List[ParseIssue],
    path: str,
) -> Dict[str, Dict[str, Any]]:
    """Validate the trap map: required fields, known radar dimension, non-empty text."""
    traps: Dict[str, Dict[str, Any]] = {}
    if raw_traps in (None, {}):
        return traps
    if not isinstance(raw_traps, dict):
        _issue(issues, "wrong_type", path, f"traps must be an object, got {type(raw_traps).__name__}")
        return traps

    for trap_id, raw in raw_traps.items():
        trap_path = f"{path}.{trap_id}"
        if not isinstance(raw, dict):
            _issue(issues, "wrong_type", trap_path, f"trap must be an object, got {type(raw).__name__}")
            continue
        for field in sorted(set(raw) - _ALLOWED_TRAP_KEYS):
            _issue(issues, "unknown_field", f"{trap_path}.{field}", f"unknown trap field '{field}'", SEVERITY_WARNING)

        record: Dict[str, Any] = {}
        for field in ("title", "desc", "prereq"):
            value = _as_text(raw.get(field))
            if not value:
                _issue(issues, "empty_trap_field", f"{trap_path}.{field}", f"trap field '{field}' must not be empty")
            record[field] = value

        radar = _as_text(_norm_key(raw, "radar_hit", "radarHit")) or "trapDefense"
        if radar not in RADAR_DIMENSIONS:
            _issue(
                issues,
                "unknown_radar_dimension",
                f"{trap_path}.radar_hit",
                f"'{radar}' is not one of {list(RADAR_DIMENSIONS)}",
            )
        record["radar_hit"] = radar
        traps[str(trap_id)] = record
    return traps


# --- Graph parsing -----------------------------------------------------------


def _parse_graph(raw_graph: Any, issues: List[ParseIssue], path: str) -> Optional[Dict[str, Any]]:
    """Validate the optional knowledge subgraph: unique node ids and resolvable edges."""
    if raw_graph is None:
        return None
    if not isinstance(raw_graph, dict):
        _issue(issues, "wrong_type", path, f"graph must be an object, got {type(raw_graph).__name__}")
        return None

    nodes = raw_graph.get("nodes") or []
    edges = raw_graph.get("edges") or []
    if not isinstance(nodes, list) or not isinstance(edges, list):
        _issue(issues, "wrong_type", path, "graph.nodes and graph.edges must be lists")
        return None

    node_ids: List[str] = []
    for index, node in enumerate(nodes):
        node_path = f"{path}.nodes[{index}]"
        if not isinstance(node, dict):
            _issue(issues, "wrong_type", node_path, "graph node must be an object")
            continue
        node_id = _as_text(node.get("id"))
        if not node_id:
            _issue(issues, "missing_field", f"{node_path}.id", "graph node id is required")
        elif node_id in node_ids:
            _issue(issues, "duplicate_graph_node", node_path, f"duplicate graph node id '{node_id}'")
        node_ids.append(node_id)

    for index, edge in enumerate(edges):
        edge_path = f"{path}.edges[{index}]"
        if not isinstance(edge, dict):
            _issue(issues, "wrong_type", edge_path, "graph edge must be an object")
            continue
        source = _as_text(edge.get("from") or edge.get("from_node"))
        target = _as_text(edge.get("to") or edge.get("to_node"))
        for endpoint, value in (("from", source), ("to", target)):
            if value and value not in node_ids:
                _issue(
                    issues,
                    "dangling_graph_edge",
                    f"{edge_path}.{endpoint}",
                    f"edge endpoint '{value}' is not a declared node id",
                )
    return {"title": _as_text(raw_graph.get("title")), "nodes": nodes, "edges": edges}


# --- Question parsing --------------------------------------------------------


def _parse_question(raw: Any, index: int, service: QuizService, issues: List[ParseIssue]) -> Optional[QuizItem]:
    """Validate one question, append issues, and return the model when it is safe to build."""
    path = f"questions[{index}]"
    if not isinstance(raw, dict):
        _issue(issues, "wrong_type", path, f"question must be an object, got {type(raw).__name__}")
        return None

    for field in sorted(set(raw) - _ALLOWED_QUESTION_KEYS):
        _issue(issues, "unknown_field", f"{path}.{field}", f"unknown question field '{field}'", SEVERITY_WARNING)

    before = len([i for i in issues if i.severity == SEVERITY_ERROR])

    question_id = _as_text(_norm_key(raw, "id", "question_id", "questionId"))
    if not question_id:
        _issue(issues, "missing_field", f"{path}.id", "question id is required")

    subject_raw = _as_text(raw.get("subject"))
    if not subject_raw:
        _issue(issues, "missing_field", f"{path}.subject", "subject is required")
        subject = ""
    else:
        subject = service.normalize_subject(subject_raw) or subject_raw.lower()
        if subject not in KNOWN_SUBJECTS:
            _issue(
                issues,
                "unknown_subject",
                f"{path}.subject",
                f"'{subject_raw}' does not resolve to one of {list(KNOWN_SUBJECTS)}",
            )

    stem = _as_text(raw.get("stem"))
    if not stem:
        _issue(issues, "missing_field", f"{path}.stem", "stem is required")

    explanation = _as_text(raw.get("explanation"))
    if not explanation:
        _issue(issues, "missing_explanation", f"{path}.explanation", "explanation must not be empty")

    answer = _as_text(raw.get("answer")) or None
    options, referenced_traps = _parse_options(raw.get("options"), answer, issues, f"{path}.options")
    traps = _parse_traps(raw.get("traps"), issues, f"{path}.traps")
    graph = _parse_graph(raw.get("graph"), issues, f"{path}.graph")

    # --- option / answer / trap cross-checks ---
    correct_keys = [opt["key"] for opt in options if opt.get("is_correct")]
    if answer:
        if options and answer.upper() not in {opt["key"] for opt in options}:
            _issue(issues, "answer_not_in_options", f"{path}.answer", f"answer '{answer}' is not one of the option keys")
        elif correct_keys and answer.upper() != correct_keys[0]:
            _issue(
                issues,
                "answer_mismatch",
                f"{path}.answer",
                f"answer '{answer}' contradicts the option marked correct ('{correct_keys[0]}')",
            )
        elif not correct_keys:
            # Materialise the flag implied by `answer` so the model is internally consistent.
            for opt in options:
                opt["is_correct"] = opt["key"] == answer.upper()

    correct_set = {opt["key"] for opt in options if opt.get("is_correct")}
    if len(correct_set) > 1:
        _issue(issues, "multiple_correct_options", f"{path}.options", f"more than one correct option: {sorted(correct_set)}")
    if options and not correct_set:
        _issue(issues, "no_correct_option", f"{path}.options", "no option is marked correct")

    for option in options:
        trap_id = option.get("trap_id")
        if option["key"] in correct_set:
            if trap_id:
                _issue(
                    issues,
                    "trap_on_correct_option",
                    f"{path}.options",
                    f"correct option {option['key']} carries trap_id '{trap_id}'",
                    SEVERITY_WARNING,
                )
            continue
        if not trap_id:
            _issue(
                issues,
                "missing_trap_id",
                f"{path}.options",
                f"distractor {option['key']} has no trap_id (every distractor must map to one trap)",
            )
        elif trap_id not in traps:
            _issue(
                issues,
                "dangling_trap_id",
                f"{path}.options",
                f"distractor {option['key']} references undefined trap '{trap_id}'",
            )

    for trap_id in sorted(set(traps) - set(referenced_traps)):
        _issue(
            issues,
            "orphan_trap",
            f"{path}.traps.{trap_id}",
            f"trap '{trap_id}' is not referenced by any option",
            SEVERITY_WARNING,
        )

    if len([i for i in issues if i.severity == SEVERITY_ERROR]) > before:
        # Do not build a model from an entry that already has hard errors: the caller wants a
        # clean list of usable questions, and a partially valid model would hide the defect.
        return None

    payload: Dict[str, Any] = {
        "id": question_id,
        "subject": subject,
        "stem": stem,
        "options": options,
        "answer": answer,
        "explanation": explanation,
        "traps": traps,
        "tag": _as_text(raw.get("tag")),
        "difficulty": _as_text(raw.get("difficulty")) or "★★★☆☆",
        "trap_hint": _as_text(_norm_key(raw, "trap_hint", "trapHint")) or None,
        "socratic_prompt": _as_text(_norm_key(raw, "socratic_prompt", "socraticPrompt")) or None,
    }
    if graph is not None:
        payload["graph"] = graph

    try:
        return QuizItem(**payload)
    except ValidationError as exc:
        _issue(issues, "model_validation_failed", path, f"could not build QuizItem: {exc.error_count()} error(s)")
        return None


# --- Public API --------------------------------------------------------------


def parse_question_pack(payload: Any) -> ParseResult:
    """Validate an already-decoded pack (a dict) and return models plus issues.

    Never raises for bad content: every problem becomes a ``ParseIssue``. A ``TypeError`` or
    ``ValueError`` here would mean the parser itself is broken, which the tests guard against.
    """
    issues: List[ParseIssue] = []
    questions: List[QuizItem] = []
    service = QuizService(questions=[])  # only used for subject normalisation

    if not isinstance(payload, dict):
        _issue(issues, "pack_not_object", "$", f"pack must be a JSON object, got {type(payload).__name__}")
        return ParseResult(questions, issues)

    version = _as_text(payload.get("schema_version"))
    if not version:
        _issue(issues, "missing_schema_version", "$.schema_version", "schema_version is recommended", SEVERITY_WARNING)
    elif version not in SUPPORTED_SCHEMA_VERSIONS:
        _issue(
            issues,
            "unsupported_schema_version",
            "$.schema_version",
            f"'{version}' is not one of {list(SUPPORTED_SCHEMA_VERSIONS)}",
            SEVERITY_WARNING,
        )

    raw_questions = payload.get("questions")
    if raw_questions is None:
        _issue(issues, "missing_field", "$.questions", "questions array is required")
        return ParseResult(questions, issues)
    if not isinstance(raw_questions, list):
        _issue(issues, "wrong_type", "$.questions", f"questions must be an array, got {type(raw_questions).__name__}")
        return ParseResult(questions, issues)
    if not raw_questions:
        _issue(issues, "pack_empty", "$.questions", "the pack contains no questions")
        return ParseResult(questions, issues)

    seen_ids: Dict[str, int] = {}
    for index, raw_question in enumerate(raw_questions):
        question = _parse_question(raw_question, index, service, issues)
        if question is None:
            continue
        if question.id in seen_ids:
            _issue(
                issues,
                "duplicate_question_id",
                f"questions[{index}].id",
                f"id '{question.id}' already used by questions[{seen_ids[question.id]}]",
            )
            continue
        seen_ids[question.id] = index
        questions.append(question)

    return ParseResult(questions, issues)


def parse_question_pack_file(path: "str | Path") -> ParseResult:
    """Read a JSON file and validate it. File and JSON errors are reported as issues, not raised."""
    issues: List[ParseIssue] = []
    file_path = Path(path)
    if not file_path.is_file():
        _issue(issues, "pack_not_found", str(file_path), "file does not exist")
        return ParseResult([], issues)
    try:
        import json

        payload = json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        _issue(issues, "pack_invalid_json", str(file_path), f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}")
        return ParseResult([], issues)
    except OSError as exc:
        _issue(issues, "pack_unreadable", str(file_path), str(exc))
        return ParseResult([], issues)
    return parse_question_pack(payload)


def export_questions_to_pack(questions: Iterable[QuizItem]) -> Dict[str, Any]:
    """Serialise questions back to the authoring format (used by the round-trip test)."""
    exported: List[Dict[str, Any]] = []
    for question in questions:
        options: List[Dict[str, Any]] = []
        for option in question.options:  # type: ignore[union-attr]
            entry: Dict[str, Any] = {"key": option.key, "text": option.text}
            if option.is_correct:
                entry["is_correct"] = True
            if option.trap_id:
                entry["trap_id"] = option.trap_id
            options.append(entry)
        traps = {
            trap_id: {
                "title": trap.title,
                "desc": trap.desc,
                "prereq": trap.prereq,
                "radar_hit": trap.radar_hit,
            }
            for trap_id, trap in (question.traps or {}).items()
        }
        exported.append(
            {
                "id": question.id,
                "subject": question.subject,
                "difficulty": question.difficulty,
                "tag": question.tag,
                "stem": question.stem,
                "options": options,
                "answer": question.answer,
                "explanation": question.explanation,
                "traps": traps,
            }
        )
    return {"schema_version": SCHEMA_VERSION, "questions": exported}

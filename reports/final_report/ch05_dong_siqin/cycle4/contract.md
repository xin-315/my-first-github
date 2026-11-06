# Interface and Data Contract — Question Pack v1.0

**Owner:** Siqin Dong (50106060) · **Cycle:** 4 · **Status:** implemented and tested
**Companion documents:** [`design_note.md`](design_note.md) (rationale and limitations),
[`samples/`](samples/) (a valid pack and a deliberately broken one)

This document is the contract an author needs in order to produce quiz content, and the
contract a reviewer needs in order to check that the implementation still honours it.

---

## 1. Pack envelope

| Field | Type | Required | Rule |
| :--- | :--- | :-: | :--- |
| `schema_version` | string | recommended | `"1.0"`. A missing or unexpected value is a **warning**, so older files still load. |
| `questions` | array | **yes** | At least one question. An empty array is rejected (`pack_empty`). |
| `description` | string | no | Free text for authors. Unknown envelope keys are ignored. |

The root must be a JSON object; a bare array is rejected (`pack_not_object`). Unknown keys inside
a *question*, *option* or *trap* produce a warning rather than an error, because they are usually
typos (`trapid`) that the author wants to see.

---

## 2. Question object

| Field | Type | Required | Rule |
| :--- | :--- | :-: | :--- |
| `id` | string | **yes** | Unique within the pack. Aliases accepted: `question_id`, `questionId`. |
| `subject` | string | **yes** | Must resolve to a known discipline code (see §5). Aliases such as `economics` are normalised. |
| `stem` | string | **yes** | Non-empty. |
| `options` | array | **yes** | Exactly four entries (see §3). |
| `answer` | string | recommended | The key of the correct option. If omitted, it is derived from the option flagged correct. If present, it must agree with that flag. |
| `explanation` | string | **yes** | Non-empty. The report claims every explanation carries an authority marker (a statutory article or a formula); the validator does **not** enforce that (§8). |
| `traps` | object | **yes** when distractors exist | Map `trap_id → TrapDetail` (see §4). Every distractor must reference an entry of this map. |
| `difficulty` | string | no | Star rating, e.g. `"★★★★☆"`. Defaults to `"★★★☆☆"`. |
| `tag` | string | no | Syllabus or examination tag. |
| `trap_hint` | string | no | Short hint for the interface. Aliases: `trapHint`. |
| `socratic_prompt` | string | no | Curated fallback wording for the Socratic guidance. Aliases: `socraticPrompt`. |
| `graph` | object | no | Optional knowledge subgraph (see §6). |

---

## 3. Option object

| Field | Type | Required | Rule |
| :--- | :--- | :-: | :--- |
| `key` | string | **yes** | The four keys must be exactly `A`, `B`, `C`, `D`. |
| `text` | string | **yes** | Non-empty. |
| `is_correct` | boolean | one option only | Exactly one option is correct. Alias: `isCorrect`. |
| `trap_id` | string | **yes for distractors** | Must exist in the question's `traps` map. The correct option must not carry one (warning). Alias: `trapId`. |

A lenient `"options": {"A": "text", ...}` mapping is also parsed, but it cannot express trap
links, so it is rejected for `missing_trap_id`. Authors should use the array form.

---

## 4. Trap object

| Field | Type | Required | Rule |
| :--- | :--- | :-: | :--- |
| `title` | string | **yes** | Names the misconception. |
| `desc` | string | **yes** | Explains what is wrong. |
| `prereq` | string | **yes** | Names the missing prerequisite. |
| `radar_hit` | string | no | One of the five dimensions in §5. Defaults to `trapDefense`. Alias: `radarHit`. |

A trap that no distractor references produces a warning (`orphan_trap`), not an error: it usually
means the author forgot to link an option.

---

## 5. Vocabularies

**Discipline codes** (`subject`) — verified against the shipped bank on 3 November 2026:

`econ`, `cs`, `law`, `se`, `or`, `mis`, `prob_stat`, `mkt`, `eng`

The bank currently holds 17 questions: law, cs, econ and se carry three each; or, mis,
prob_stat, mkt and eng carry one each. `KNOWN_SUBJECTS` in the parser must be extended when a
new discipline is authored, and a drift test fails until it is.

**Radar dimensions** (`radar_hit`) — the five dimensions of the mastery dashboard:

`recall`, `boundary`, `trapDefense`, `synthesis`, `precision`

The spelling is case-sensitive: `trap_defense` is rejected, exactly as the report's data rules
require.

---

## 6. Optional knowledge subgraph

```json
"graph": {
  "title": "Revocation period subgraph",
  "nodes": [{"id": "n_core", "label": "Revocation period", "type": "core", "x": 0, "y": 0}],
  "edges": [{"from": "n_core", "to": "n_core", "label": "precondition"}]
}
```

Rules: node ids must be unique (`duplicate_graph_node`), and every edge endpoint must name a
declared node (`dangling_graph_edge`). Nodes and edges are passed through unchanged.

---

## 7. Parser interface

```python
from backend.app.services.question_parser import parse_question_pack, parse_question_pack_file

result = parse_question_pack_file("packs/law.json")
result.ok                # bool  -> True when there are no errors (warnings allowed)
result.questions         # list[QuizItem]
result.issues            # list[ParseIssue]
result.errors            # list[ParseIssue]  (severity == "error")
result.warnings          # list[ParseIssue]  (severity == "warning")
result.codes()           # sorted unique codes, convenient for assertions

for issue in result.issues:
    print(issue.code, issue.path, issue.message, issue.severity)
```

`ParseIssue` is a small object with `code`, `path`, `message`, `severity`, plus `render()` for
logs and `to_dict()` for machine output. `ParseResult` also exposes `to_dict()`.

Parsing **does not raise** for bad content: every defect becomes an issue. `ParseIssue` and
`ParseResult` are returned for all inputs, including a missing file or invalid JSON.

---

## 8. CLI contract

```
python scripts/validate_question_pack.py PACK [--json] [--strict] [--diagnose QID:KEY] [--export PATH]
```

| Option | Effect |
| :--- | :--- |
| *(none)* | Human-readable report: verdict, counts, every issue, accepted ids |
| `--json` | Machine-readable `ParseResult.to_dict()` on stdout |
| `--strict` | Warnings become failures (exit 1) |
| `--diagnose QID:KEY` | Run the diagnosis engine on the parsed pack and print the response fields |
| `--export PATH` | Write the normalised pack that would be loaded |

| Exit code | Meaning |
| :-: | :--- |
| 0 | pack is usable |
| 1 | pack has errors (or, with `--strict`, warnings), or the file cannot be read |
| 2 | the validator itself failed unexpectedly |

---

## 9. Sample cases

### 9.1 Accepted (excerpt of `samples/valid_pack.json`, exported from the real bank)

```json
{
  "schema_version": "1.0",
  "questions": [
    {
      "id": "law_1",
      "subject": "law",
      "difficulty": "★★★☆☆",
      "tag": "可撤销民事法律行为 · 撤销权存续期间",
      "stem": "甲于2023年3月1日因受欺诈与乙签订二手车买卖合同……",
      "options": [
        {"key": "A", "text": "自合同签订之日……3 年内届满", "trap_id": "trap_law_1"},
        {"key": "B", "text": "自知道受欺诈之日……1 年内届满", "is_correct": true},
        {"key": "C", "text": "自欺诈行为终止之日起算……", "trap_id": "trap_law_2"},
        {"key": "D", "text": "自合同签订之日起算……2 年内届满", "trap_id": "trap_law_3"}
      ],
      "answer": "B",
      "explanation": "【权威考点解析 · 民法典第152条】……",
      "traps": {
        "trap_law_1": {"title": "…", "desc": "…", "prereq": "…", "radar_hit": "trapDefense"}
      }
    }
  ]
}
```

Observed CLI result:

```
verdict   : OK
questions : 2 accepted
issues    : 0 error(s), 0 warning(s)
accepted ids: law_1, cs_2
```

### 9.2 Rejected (`samples/invalid_pack.json`)

Observed CLI result (13 issues, abridged to 6):

```
verdict   : REJECTED
questions : 0 accepted
issues    : 12 error(s), 1 warning(s)
  [error]   unknown_subject      questions[0].subject: 'astrology' does not resolve to one of [...]
  [error]   missing_explanation  questions[0].explanation: explanation must not be empty
  [error]   option_count         questions[0].options: expected 4 options, found 3
  [error]   unknown_radar_dimension questions[0].traps.trap_1.radar_hit: 'trap_defense' is not one of [...]
  [error]   dangling_trap_id     questions[0].options: distractor A references undefined trap 'trap_missing'
  [warning] orphan_trap          questions[0].traps.trap_1: trap 'trap_1' is not referenced by any option
```

The full list is reproduced by running the CLI; every issue names the exact path so the author
can fix them in one pass.

### 9.3 End-to-end (parse → diagnose)

```
$ python scripts/validate_question_pack.py samples/valid_pack.json --diagnose law_1:A
diagnosis : law_1:A
  is_correct      : False
  correct_key     : B
  trap_title      : 🚨 典型混淆陷阱：把'形成权除斥期间'错套为'3年普通诉讼时效'
  concept_name    : 先修定理前置：请求权 vs 形成权区别与法定除斥期间
  radar_dimension : trapDefense
  fallback_mode   : True
  model_used      : local-knowledge-seed
```

With a live API key the same call reports `fallback_mode: False` and `model_used: qwen-turbo`;
without one it degrades to the curated wording. The diagnosis verdict is unchanged either way,
because the verdict comes from the data and not from the model.

---

## 10. Guarantees and non-guarantees

**Guaranteed by the parser**

- A pack that passes validation contains only questions with four options, exactly one correct
  option, a resolvable trap for every distractor, non-empty trap fields, a known radar dimension
  and a non-empty explanation.
- Every defect is reported with a stable code and a path; the parser never raises for bad content.
- The shipped bank passes the same rules (round-trip test).

**Not guaranteed**

- That the content is *pedagogically* correct: the parser checks structure and references, not
  whether a trap is a good trap.
- That every explanation carries an authority marker (see §8 of the design note).
- Performance at scale: the parser is linear in questions and was not benchmarked.

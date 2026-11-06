# Cycle 4 Design Note — Question Parsing and Misconception Diagnosis Slice

**Owner:** Siqin Dong (50106060), PoC Logic Developer
**Cycle:** Cycle 4 (3–30 November 2026)
**Checkpoint:** 1 — agree the bounded slice, acceptance criteria and technical approach (3–7 November)
**Status:** slice implemented and tested locally; not yet merged

---

## 1. Problem

Quiz content can currently only be added by editing `backend/app/data/seed_questions.py` by
hand. That has three costs:

1. **Authoring requires a Python developer.** A business analyst cannot add or correct a
   question without touching source code.
2. **Defects surface late.** A distractor that points at a trap which does not exist, a question
   with two correct options, or a trap with an empty prerequisite is only discovered when the
   diagnosis request is served — or never, if nobody happens to pick that option.
3. **No machine-readable contract.** There is no artefact that says what a valid question is,
   so content review depends on memory and on reading the Python file.

The data rules themselves already exist and are described in the Technical Report (Chapter
5.3.4); what is missing is an **enforcement point at ingestion time**.

## 2. Scope

**In scope**

- Define an authoring format for quiz content (JSON, versioned).
- Parse it into the existing `QuizItem` domain model.
- Validate the data rules that the diagnosis engine depends on, reporting **every** problem in
  one run, each with a stable code and a JSON path.
- Exercise the diagnosis engine against the parsed pack, so the slice is demonstrable end to
  end.

**Out of scope (deliberately)**

- No new API endpoint. The slice is exercised through a CLI and tests; the HTTP surface stays
  unchanged, so no frontend work and no contract change is required.
- No database, queue or upload UI.
- No authoring of new question content: the sample pack is exported from the existing bank.
- No change to diagnosis rules or to the radar aggregation.

## 3. Input and output

| | |
| :--- | :--- |
| **Input** | A UTF-8 JSON file: `{"schema_version": "1.0", "questions": [ ... ]}`. Each question supplies `id`, `subject`, `stem`, four `options`, `answer`, `explanation` and a `traps` map. snake_case and camelCase keys are both accepted. |
| **Output (success)** | `ParseResult` with typed `QuizItem` models (`result.questions`), `result.ok == True`, and no errors. |
| **Output (failure)** | `ParseResult` with `result.issues`: each issue carries `code`, `path`, `message`, `severity`. `result.ok == False`. No exception is raised for bad content. |
| **CLI output** | A human-readable report, or `--json` for machine consumption. Exit code 0 (usable), 1 (rejected), 2 (validator failure). |
| **Diagnosis demo** | `--diagnose QUESTION_ID:OPTION` runs the real engine on the parsed pack and prints `is_correct`, `correct_key`, `trap_title`, `concept_name`, `radar_dimension`, `fallback_mode`, `model_used` and the first 160 characters of the guidance. |

## 4. Failure cases

Each code below is a rule, not an implementation detail. All errors are collected in a single
pass; the pack is rejected if any error is present.

| Code | Severity | Meaning |
| :--- | :--- | :--- |
| `pack_not_object` | error | the file's root is not a JSON object |
| `missing_field` | error | a required field is absent (`questions`, `id`, `subject`, `stem`) |
| `pack_empty` | error | `questions` is an empty array |
| `pack_not_found` / `pack_unreadable` / `pack_invalid_json` | error | the file cannot be read or decoded |
| `wrong_type` | error | a field has the wrong JSON type |
| `duplicate_question_id` | error | two accepted questions share one id |
| `unknown_subject` | error | the subject does not resolve to a known discipline code |
| `option_count` | error | the question does not have exactly four options |
| `option_keys_invalid` | error | the option keys are not exactly A–D |
| `duplicate_option_key` | error | two options share a key |
| `invalid_option_key` | error | a key is not a single letter |
| `empty_option_text` | error | option text is blank |
| `no_correct_option` / `correct_option_count` | error | zero or more than one correct option |
| `multiple_correct_options` | error | more than one option is flagged correct |
| `answer_not_in_options` | error | `answer` does not match any option key |
| `answer_mismatch` | error | `answer` contradicts the option flagged correct |
| `missing_trap_id` | error | a distractor has no trap link |
| `dangling_trap_id` | error | a distractor references a trap that is not defined |
| `empty_trap_field` | error | `title`, `desc` or `prereq` is blank |
| `unknown_radar_dimension` | error | `radar_hit` is not one of the five dimensions |
| `missing_explanation` | error | the explanation is blank |
| `dangling_graph_edge` / `duplicate_graph_node` | error | the optional knowledge subgraph is inconsistent |
| `model_validation_failed` | error | the domain model rejected the entry (safety net) |
| `missing_schema_version` / `unsupported_schema_version` | warning | the envelope version is absent or unexpected |
| `unknown_field` | warning | an unrecognised key (usually a typo such as `trapid`) |
| `orphan_trap` | warning | a trap is defined but no option references it |
| `trap_on_correct_option` | warning | the correct option carries a trap link |

## 5. Acceptance criteria (testable)

| # | Criterion | Evidence |
| :-: | :--- | :--- |
| A1 | A well-formed pack yields typed models and `ok == True` | `test_valid_pack_is_accepted` |
| A2 | The real shipped bank survives export → parse with no issues | `test_real_seed_bank_round_trips` |
| A3 | Every failure code above is produced by at least one test | 30+ assertions in `tests/test_question_parser.py` |
| A4 | All problems in a pack are reported in one run | `test_all_errors_are_reported_not_just_the_first` |
| A5 | Warnings do not block; `--strict` promotes them | `test_orphan_trap_is_a_warning_only`, `test_cli_strict_promotes_warnings` |
| A6 | CLI exit codes are 0 / 1 as documented | `test_cli_accepts_a_valid_pack`, `test_cli_rejects_an_invalid_pack` |
| A7 | A parsed pack can be diagnosed without touching the seed repository | `test_diagnosis_runs_on_a_parsed_pack` |
| A8 | An unknown question id still degrades gracefully | `test_diagnosis_of_an_unknown_question_degrades_gracefully` |
| A9 | The default engine keeps its previous behaviour | `test_default_engine_still_uses_the_seed_repository` |
| A10 | The full suite passes | 232 passed (183 before this slice, 49 added) |

## 6. Alternatives considered

| Alternative | Why it was rejected |
| :--- | :--- |
| Validate inside the `/api/diagnose` handler | The failure would still reach production content, and it would couple validation to the request path instead of the ingestion path. |
| Rely on Pydantic model construction alone | Pydantic reports a single nested `ValidationError` with internal type names. It cannot express rules such as "every distractor maps to a declared trap", and it aborts on the first failure, which makes content review slow. |
| A JSON Schema file plus a generic validator | JSON Schema can express types and required fields, but not cross-field semantics (trap references, answer consistency, radar vocabulary) without unreadable conditional schemas. A small explicit validator is easier to review and to extend. |
| Add a `POST /api/questions/validate` endpoint | It changes the API contract and needs frontend work, which is outside this slice. The CLI covers the same use case for authors and for CI. |

## 7. Affected files

| File | Change |
| :--- | :--- |
| `backend/app/services/question_parser.py` | **new** — pack parsing, validation, issue codes, export helper |
| `backend/app/services/diagnostic_service.py` | small change — optional `quiz_repo` injection so a parsed pack can be diagnosed; default behaviour unchanged |
| `scripts/validate_question_pack.py` | **new** — CLI entry point |
| `tests/test_question_parser.py` | **new** — 49 tests |
| `reports/final_report/ch05_dong_siqin/cycle4/` | **new** — this note, the contract, sample packs, the viva notes |

## 8. Verification performed

```
python -m pytest tests -q         -> 232 passed
python scripts/validate_question_pack.py <valid_pack>    -> exit 0, 2 questions accepted
python scripts/validate_question_pack.py <invalid_pack>  -> exit 1, 12 errors + 1 warning
python scripts/validate_question_pack.py <valid_pack> --diagnose law_1:A
   -> is_correct False, trap_title resolved, fallback_mode True, model_used local-knowledge-seed
```

## 9. Limitations and unresolved questions

1. **Duplicate ids are only detected among questions that pass validation.** If both copies of a
   duplicated id are otherwise invalid, the duplicate is not reported separately. Acceptable for
   now because both entries are rejected anyway; a pack-level id scan would close the gap.
2. **The authority marker is not enforced.** The report claims that every explanation carries a
   statutory article or a formula. Detecting "has a citation" reliably needs a policy decision
   (regex would produce false positives), so it is left as a review task.
3. **The subject vocabulary is a constant.** `KNOWN_SUBJECTS` must be extended when a new
   discipline is authored; a drift test fails until it is, which is intentional.
4. **The stored bank has drifted from the Chapter 5.3 numbers.** On 3 November 2026 the bank
   holds 17 questions across 9 disciplines (law/cs/econ/se: 3 each; or/mis/prob_stat/mkt/eng: 1
   each) and 51 traps. Chapter 5.3 reports 12 questions / 4 disciplines / 36 traps, which was
   accurate at the frozen Cycle 3 baseline. Any new claim must use the current numbers.
5. **No performance claim.** The parser is linear in the number of questions and was not
   benchmarked; no latency figure is claimed here.

## 10. Next checkpoint (by 15 November)

- Add the pack-level duplicate scan (limitation 1) and a test for it.
- Decide with Yusai Xi whether the authoring format should carry the UI copy (option labels,
  empty-state text), or whether the dashboard contract stays separate.
- Agree the mastery-dashboard data contract fields (`radar_hit` vocabulary is the shared part)
  and record the agreed shape in `contract.md`.

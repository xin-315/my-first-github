# Cycle 4 — Understanding Checkpoint Notes (Siqin Dong)

The assignment asks each owner to explain, in English: the problem, how the code works, why this
approach was chosen, what the tests demonstrate and do not demonstrate, and one failure or
limitation. This file is the script for that conversation.

---

## 1. What problem does the change address?

Quiz content could only be added by editing `backend/app/data/seed_questions.py` by hand. Three
consequences: only a Python developer could author a question, a broken entry (a distractor
pointing at a trap that does not exist, two correct options, an empty prerequisite) was only
discovered when a student happened to pick that option, and there was no artefact that defined
what valid content is.

The change adds an **ingestion gate**: a JSON authoring format plus a validator that enforces the
data rules and reports every defect with a code and a path, before the content reaches the
diagnosis engine.

## 2. How does the code work?

```
scripts/validate_question_pack.py            CLI: read path, print report, exit 0/1/2
        └── question_parser.parse_question_pack_file()
                └── parse_question_pack(payload)          envelope checks, id de-duplication
                        └── _parse_question(raw, index)    one question at a time
                                ├── _parse_options()       exactly A–D, one correct, trap link
                                ├── _parse_traps()         four fields, radar vocabulary
                                ├── _parse_graph()         optional, edges must resolve
                                └── QuizItem(**payload)    existing Pydantic domain model
```

Every check appends a `ParseIssue(code, path, message, severity)` to one list. A question is only
built into a `QuizItem` if it accumulated no errors, so `result.questions` is a list of entries
that are safe to serve. Warnings (typos, orphan traps) do not block.

The diagnosis part reuses the existing engine through one small change: `DiagnosticService` now
accepts an optional `quiz_repo`, so the CLI can build `QuizService(result.questions)` and diagnose
the parsed pack without touching the process-wide seed repository. The default is unchanged.

## 3. Why this approach, and what alternative was considered?

**Chosen:** a small explicit validator over the existing Pydantic models, driven by a CLI.

**Rejected:** validating with Pydantic alone. Pydantic validates types and single-field
constraints, but the important rules here are cross-field: "every distractor references a trap
that exists in this question", "the answer agrees with the option flagged correct", "the radar
dimension is one of five". Pydantic also aborts on the first failure and reports internal type
names, which is poor feedback for an author who needs to fix ten things at once.

**Also rejected:** a JSON Schema file plus a generic validator. Cross-field rules would need
conditional schemas that are harder to review than forty lines of explicit code, and the schema
would still not express "referenced trap must be declared in the same question".

**Also rejected:** a `POST /api/questions/validate` endpoint. It changes the HTTP contract and
needs frontend work; the CLI covers authors and CI without touching the API surface.

## 4. What do the tests demonstrate, and what do they not?

They demonstrate that: a well-formed pack becomes typed models; the shipped bank survives
export → parse unchanged; each documented failure code is actually produced (one test per code
class); all defects are reported in a single run; warnings do not block while `--strict` promotes
them; the CLI exit codes match the contract; a parsed pack can be diagnosed end to end; an unknown
question id still degrades gracefully; and the default engine keeps its previous behaviour.

They do **not** demonstrate that a trap is pedagogically good, that the content is correct, that
every explanation carries a cited authority (not enforced), or anything about performance at
scale. The suite also cannot prove that no other code path bypasses the parser.

## 5. One failure, limitation or unresolved question

`duplicate_question_id` is only detected among questions that already pass validation. If both
copies of a duplicated id are otherwise invalid, the duplicate is not reported separately, because
the second entry never becomes a model. It is not harmful today (both entries are rejected), but a
pack-level id scan would close the gap, and that is my next checkpoint task.

## 6. Numbers I must be able to quote (verified 3 November 2026)

| Fact | Value | Source |
| :--- | :--- | :--- |
| Questions in the shipped bank | **17** | `backend/app/data/seed_questions.py` |
| Disciplines | **9** — law, cs, econ, se (3 each); or, mis, prob_stat, mkt, eng (1 each) | same |
| Traps | **51**, exactly **3 per question** | same |
| Radar distribution | `boundary` 17, `recall` 13, `trapDefense` 12, `synthesis` 7, `precision` 2 | same |
| Test suite | **232 passed** (183 before this slice, **49** added) | `python -m pytest tests -q` |
| Failure codes implemented | 24 error codes, 5 warning codes | `backend/app/services/question_parser.py` |

Note: Chapter 5.3 of the Technical Report states 12 questions / 4 disciplines / 36 traps. That was
accurate at the frozen Cycle 3 baseline; the bank has since grown. Any new claim must use the
current numbers above.

## 7. Likely follow-up questions

**"Convince me the rules are enforced, not just documented."**
Run `python scripts/validate_question_pack.py reports/final_report/ch05_dong_siqin/cycle4/samples/invalid_pack.json`.
It exits 1 and lists twelve errors with paths. The valid pack exits 0.

**"What happens if someone renames a radar dimension in the frontend?"**
The drift test `test_known_subjects_cover_the_seed_bank` catches subject drift; the radar
vocabulary is a constant, so a rename fails tests that assert the five dimensions, and the
validator rejects content using an unknown value (`unknown_radar_dimension`). The dimension names
are part of the dashboard data contract and are agreed with Yusai Xi.

**"Why does the parser not reject an unknown field?"**
Because a typo is usually recoverable and the author benefits from seeing it without the pack
being blocked; it is reported as a warning, and `--strict` turns it into a failure for CI.

**"What is not covered yet?"**
Pack-level duplicate detection for invalid entries, an authority-marker check, and any performance
claim. All three are recorded in `design_note.md` §9.

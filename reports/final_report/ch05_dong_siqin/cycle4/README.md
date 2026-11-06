# Cycle 4 — Question Parsing and Misconception Diagnosis Slice

**Owner:** Siqin Dong (50106060) · **Cycle:** 4 (3–30 November 2026) · **Checkpoint 1:** 3–7 November

This folder holds the evidence for my Cycle 4 assignment: *"Define the question-parsing and
misconception-diagnosis slice; document its input, output, and failure cases."*

---

## 1. Deliverables against the assignment

| Required evidence | Where it is | Status |
| :--- | :--- | :--- |
| A short design note (problem, expected behaviour, affected files, acceptance criteria) | [`design_note.md`](design_note.md) | Done |
| One working vertical slice | `backend/app/services/question_parser.py` + `scripts/validate_question_pack.py` + `diagnostic_service` injection | Done, demonstrated below |
| Tests for representative valid and invalid inputs | `tests/test_question_parser.py` (49 tests) | Done, all passing |
| A documented interface / data contract with sample cases | [`contract.md`](contract.md) + [`samples/`](samples/) | Done |
| Preparation for the understanding checkpoint | [`viva_cycle4.md`](viva_cycle4.md) | Done |
| Coordination with Yusai Xi on quiz content and the mastery-dashboard contract | `contract.md` §5 (shared radar vocabulary); meeting note pending | In progress |

## 2. Reproduce it

All commands run from the repository root.

```powershell
# 1) full test suite (232 expected: 183 baseline + 49 new)
python -m pytest tests -q

# 2) validate a good pack
python scripts/validate_question_pack.py reports/final_report/ch05_dong_siqin/cycle4/samples/valid_pack.json
#    -> verdict OK, 2 questions accepted, exit 0

# 3) validate a deliberately broken pack
python scripts/validate_question_pack.py reports/final_report/ch05_dong_siqin/cycle4/samples/invalid_pack.json
#    -> verdict REJECTED, 12 errors + 1 warning with paths, exit 1

# 4) the whole slice: parse the pack, then diagnose one option
python scripts/validate_question_pack.py reports/final_report/ch05_dong_siqin/cycle4/samples/valid_pack.json --diagnose law_1:A
#    -> is_correct False, trap_title resolved, radar_dimension trapDefense, fallback_mode True

# 5) machine-readable output (for CI or another tool)
python scripts/validate_question_pack.py reports/final_report/ch05_dong_siqin/cycle4/samples/valid_pack.json --json
```

## 3. What the slice proves

- A JSON pack is parsed into the existing `QuizItem` domain model; the shipped bank round-trips
  through export → parse with zero issues.
- Every data rule the diagnosis engine depends on is enforced at ingestion, with a stable error
  code and a JSON path per defect, and **all** defects are reported in one run.
- The diagnosis engine runs against the parsed pack, so the path from authoring file to teaching
  feedback is demonstrable end to end.
- Failure behaviour is explicit: an unknown question id degrades to a fallback response, and bad
  content never raises.

## 4. What it does not prove

- That a trap is pedagogically good, or that the content is correct.
- That every explanation carries a cited authority (not enforced; recorded as a review task).
- Any performance claim: the parser is linear in questions and was not benchmarked.
- That no other code path bypasses the parser (the seed bank is still loaded directly by
  `QuizService`).

## 5. Next checkpoint (by 15 November)

1. Add a pack-level duplicate-id scan and a test for it (see `design_note.md` §9 limitation 1).
2. Agree the authoring format with Yusai Xi: does the pack carry UI copy, or does the dashboard
   contract stay separate?
3. Record the agreed mastery-dashboard data contract in `contract.md` §5.

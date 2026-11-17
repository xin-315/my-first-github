# Contribution record

Mingjie Yang (50106061)

Work status: `IN PROGRESS`  
Understanding checkpoint: `NEEDS REVIEW` — explanation and demonstration pending.

## 15 November 2026

This submission checks the backend path from a question pack to a diagnosis response. The starting point was the merged parser and CLI from PR #25. The unchanged suite passed all 232 existing cases.

The added tests cover option-to-trap mapping, HTTP request and response fields, separate question repositories, simulated provider failures, and CLI behaviour in a separate process. Of the 30 added cases, 26 passed. Four expected failures reproduce two issues: invalid UTF-8 handling and optional fields lost during export. The same results were reproduced in a second clean source checkout using the same isolated Python environment. Details are in `results.md`.

The parser, CLI and existing question content are team work. This contribution is the additional verification and its documentation. Personal review and the English demonstration are still pending.

## Evidence for the assignment

| Requirement | File |
|---|---|
| Plan before implementation | `test_plan.md` |
| Backend, integration and failure tests | `tests/test_cycle4_integration.py` at the repository root |
| Repeatable run from a clean checkout | `README.md`, `run_checks.py`, `requirements-test-lock.txt` |
| Recorded results | `evidence/`, including the second checkout under `evidence/clean/` |
| What each added test proves and does not prove | `test_matrix.md` |
| Known problems and coverage limits | `results.md` |
| Preparation for the English walkthrough | `viva.md` |

## Next checkpoint

Reviewer and date: pending.

The demonstration should follow one sample through parsing and diagnosis, show a passing test and an expected failure, and explain the limits of the simulated API checks. The reviewer can then record the outcome and any follow-up work. `UNDERSTOOD` has not been recorded.

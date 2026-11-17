# Cycle 4: backend and integration verification

Mingjie Yang (50106061) · 15 November 2026

Work status: `IN PROGRESS`. Understanding checkpoint: `NEEDS REVIEW` — English explanation and demonstration pending.

## What this submission covers

The [assignment](../../../cycle4_task_assignment_2026-11-03.md) gives me responsibility for backend and integration tests, including failure cases. This submission checks the parser and diagnosis workflow merged in PR #25, at commit `5687727e903311a081896208e800e1d0f6c322cf`.

The parser, CLI, sample packs and 232 existing tests were already in the repository. The additions here are 30 test cases, a script to repeat the runs, and the results. The tests use those existing packs and seed questions. Negative cases change a copy of an existing input or simulate a service failure.

See [plan](test_plan.md), [per-case matrix](test_matrix.md), [results and limitations](results.md), [English walkthrough](viva.md), and [contribution record](contribution.md).

## Clean-checkout instructions

Use Python 3.12 (verified here on Windows). Start from the repository root, without a `.env` file. The test-only lock installs the backend verification dependencies, not the complete UI, Neo4j, document or GraphRAG toolchain. No live API key is required. Do not upload a virtual environment.

```powershell
git clone https://github.com/xin-315/my-first-github.git
cd my-first-github
git checkout 5687727e903311a081896208e800e1d0f6c322cf
# Overlay this submission's tests/ and reports/ directories, preserving their paths.
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r reports/final_report/ch06_yang_mingjie/cycle4/requirements-test-lock.txt
.venv/Scripts/python.exe reports/final_report/ch06_yang_mingjie/cycle4/run_checks.py verification-output
```

The checkout above intentionally pins the evidence base. For submission use a new branch based on current upstream master, then rerun if upstream production code differs. Once this PR is merged, a normal checkout of the merge commit includes the tests without overlay.

On this hardened Windows host `venv`'s `ensurepip` failed with a temporary-directory PermissionError. The interpreter was created; installing through the bundled interpreter's `pip --python <venv-python> install ...` with permission resolved it. A local Git clone also needed permission for Git's subprocess pipe. These are observed host setup limitations, not product test failures. Do not assume the workaround is necessary on other hosts.

Expected at this base: personal `26 passed, 4 xfailed`; full `258 passed, 4 xfailed`. Expected failures are unresolved product limitations, not passes. `strict=True` turns a later unexpected pass into a suite failure so the issue and test must be reviewed. A successful pytest exit alone does not mean every product expectation was satisfied.

## Demonstration

```powershell
.venv/Scripts/python.exe -m pytest tests/test_cycle4_integration.py -q -rx --disable-warnings
.venv/Scripts/python.exe scripts/validate_question_pack.py reports/final_report/ch05_dong_siqin/cycle4/samples/valid_pack.json --diagnose cs_2:B
.venv/Scripts/python.exe scripts/validate_question_pack.py reports/final_report/ch05_dong_siqin/cycle4/samples/invalid_pack.json --json
```

The valid demonstration exits 0 and uses local knowledge fallback for the wrong answer. The invalid demonstration exits 1. The HTTP tests replace the router's service only inside tests: there is no implemented production upload endpoint demonstrated by these tests.

## Remaining work

The two issues in `results.md` need review with the parser owner. These results apply to the parser/diagnosis code available on 15 November; tests will need to be rerun as later changes are integrated. GraphRAG, dashboard behaviour and user trials are outside this run.

The English explanation and live demonstration are still pending. The review status and next steps are recorded in [contribution.md](contribution.md).

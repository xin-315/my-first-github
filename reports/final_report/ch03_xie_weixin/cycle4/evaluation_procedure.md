# Reproducible evaluation procedure

## 1. Purpose and boundary

Verify the shipped JSON-pack parser, its service hand-off and the deterministic local diagnosis mapping. Independently check reporting claims and request contracts. This evaluation measures implementation behaviour; it does not measure teaching effectiveness, independent subject accuracy, retrieval quality or hallucination reduction.

Baseline: `5687727e903311a081896208e800e1d0f6c322cf`. Executed on Linux-6.18.57-x86_64-with-glibc2.41 with Python 3.12.14; exact package versions are in `evidence/review-requirements.txt`. The environment started in a new virtual environment. Only API/test dependencies were installed; Streamlit and Neo4j exploration tools were not assessed. Dependencies originally had lower bounds, so the snapshot is supplied for repeatability.

## 2. Inputs and acceptance rules

Inputs: all 17 shipped questions in `backend/app/data/seed_questions.py`, all 68 options, and the two committed JSON packs in `reports/final_report/ch05_dong_siqin/cycle4/samples/`. Exact sample hashes are recorded in the raw JSON.

| Check | Predefined expectation | What it proves |
| --- | --- | --- |
| Full existing suite | No failed tests | Existing assertions hold in the recorded environment |
| Every shipped correct option | HTTP 200 and is_correct=true | Agreement with stored answer flags |
| Every shipped distractor | HTTP 200, is_correct=false; exact trap ID, misconception and prerequisite; non-empty local guidance | Agreement with authored mappings |
| Valid sample | 2 accepted questions; no errors/warnings; CLI exit 0 | Sample satisfies implemented parser rules |
| Invalid sample | No accepted questions; 12 errors, 1 warning; CLI exit 1 | Sample defects are rejected and reported |
| Boundary probes | Record actual responses; compare with report contracts | Behaviour/documentation discrepancies; not automatic acceptance |
| Reporting probe | Compare summary before/after three wrong attempts, excluding timestamps | Whether this API summary changes for these submissions |
| Optional provider path | Synthetic key + mocked provider; record await count | Whether the provider branch is reachable, without making a live call |

Inputs are fixed by the reviewed commit. This is an exhaustive in-bank consistency check, not a held-out generalisation benchmark. Never report 68/68 as independent educational accuracy.

## 3. Setup and execution

From a clean clone, use a disposable branch at the reviewed baseline. Place this delivery's `cycle4/` directory at the same repository-relative path. Do not overwrite unrelated local work. The supplied patch adds the review and links; it contains no product implementation change.

```bash
git clone https://github.com/xin-315/my-first-github.git
cd my-first-github
git switch -c review-cycle4-xie 5687727e903311a081896208e800e1d0f6c322cf
python -m venv .venv
```

Activate with `.venv\Scripts\Activate.ps1` in Windows PowerShell or `source .venv/bin/activate` in bash. Then run:

```bash
python -m pip install -r reports/final_report/ch03_xie_weixin/cycle4/evidence/review-requirements.txt
```

For the full suite, clear model credentials **before Python starts**. In PowerShell:

```powershell
$env:QWEN_API_KEY = ""
$env:DASHSCOPE_API_KEY = ""
```

In bash:

```bash
export QWEN_API_KEY=""
export DASHSCOPE_API_KEY=""
```

Use a fresh clone without an application `.env` file so dotenv cannot restore a different credential. No paid API calls are needed.

```bash
python -m pytest tests -q --junitxml=reports/final_report/ch03_xie_weixin/cycle4/evidence/pytest.xml > reports/final_report/ch03_xie_weixin/cycle4/evidence/pytest.txt 2>&1
python reports/final_report/ch03_xie_weixin/cycle4/run_review.py
```

The review script always clears `settings.QWEN_API_KEY` in its process. The optional provider probe substitutes an AsyncMock and a synthetic key; it never submits that key to a provider. Exit 0 means all 68 option consistency checks passed; it does not mean all review findings are resolved. Read `review_results.json` and the review log even after exit 0.

Output paths are overwritten on rerun; retain a copy of earlier evidence if comparing runs. The recorded commit is the base HEAD used for this run; review files were uncommitted additions. Input/source hashes identify the evaluated files independently.

## 4. Recorded results (9 November 2026)

- Full suite: 232 passed, 17 warnings, 1.69 seconds. See `pytest.txt` and `pytest.xml`. Warnings remain visible; the suite was not edited to make it pass.
- Bank: 17 questions, 9 subjects, 51 traps. All 68 option responses match; 51 are wrong-option mappings.
- Parser: valid sample 2 accepted, no issues, exit 0; invalid sample 0 accepted, 12 errors/1 warning, exit 1.
- API filters: `subject=law` returns 3; `category=law` returns 17 because that is not the implemented filter parameter; unknown subject returns 0.
- Invalid question, invalid option E, empty object and lowercase a all returned HTTP 200 in these probes. Lowercase a normalised to A. An unknown question returned a fallback containing correct_key B; that value is not a verified answer.
- Report summary was unchanged after three wrong attempts, excluding generated timestamps; POST `/api/reports/reset` returned 405. Source inspection finds no matching reset API route; the static catch-all affects the returned status.
- Synthetic provider probe: 1 mocked call, fallback_mode=false. No live generation was evaluated.

The separately preserved [15 November rerun evidence](evidence/2026-11-15/) reproduced the same test, option and parser outcomes. See the [checkpoint summary](checkpoint_2026-11-15.md). The durations and latency values below describe the original 9 November run; current timing samples are in the dated rerun JSON.

## 5. Timing protocol

The review runs 10 warm-up calls, followed by 100 sequential TestClient requests for law_1:A with include_socratic=false. Timing uses perf_counter_ns around the complete in-process TestClient call. Median is the sample median; p95 uses the nearest-rank value at ceil(0.95*n). Raw samples are preserved.

Observed median: **1.556 ms**; observed p95: **2.021 ms**. This includes local client/framework overhead. It excludes real TCP transfer, browser rendering, server startup and cloud-model delay. Host load and package versions can change the numbers. It does not establish the report's server-startup or network-latency targets.

## 6. Baseline-versus-retrieval protocol for future execution

The following is a specified protocol, not a completed experiment. Before making accuracy or hallucination-improvement claims:

1. Freeze a bounded, independently checked dataset and separate authoring/retrieval material from held-out questions. Record item IDs, sources, split hashes and exclusion decisions.
2. Compare the same model/version under baseline and retrieval-assisted conditions. Hold prompts, temperature, token budget, answer parsing and retry policy constant except for the retrieved evidence. Save the graph/index and retrieval parameters.
3. Submit the same held-out items to both conditions; define repeat count, seeds where supported and treatment order before collecting outputs. Preserve failures and timeouts, not just successful examples.
4. Score correctness against an independently reviewed key. Define a separate hallucination rubric and evidence-adherence rubric. Use blinded human review where required and record disagreements. Do not equate answer accuracy with hallucination rate.
5. Report counts, denominators, abstentions, latency, failures and paired item-level differences, with uncertainty and subject-level limits. Preserve raw responses and model settings without credentials.
6. Review contamination and whether the local lookup bank contains evaluated answers. A comparison against a system reading its own stored answers cannot establish general superiority over a held-out baseline.

Current status: not executed. `audit_online_baseline.py` has skip handling and a live-path placeholder; it does not implement this experiment.

## 7. Remaining acceptance work

A browser walkthrough is still needed for attempt locking, keyboard access, screen-reader labels, requested explanations, history and responsive layouts. Air-gapped browser operation needs a fresh cache and blocked external networking, especially because ECharts comes from a CDN. This run used local in-process clients and did not disable host networking. These remain UNVERIFIED rather than assumed passes.

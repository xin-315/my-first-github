# Sources and provenance

## Primary existing material

- GitHub repository: https://github.com/xin-315/my-first-github
- Primary snapshot: sync/cycle3-final ae7ab47c6ff77b17f0ca62836b2c01e36da57187, retrieved 29 October 2026.
- Comparison snapshot: master 10f20657a85b6ad9d54572d1b60a67b655896f36.
- Official course brief: docs/course/2026-27-GroupProjectDescription-and-Requirements.txt, pages 4 to 8. It requires functional and non-functional evaluation, A4, 2.54 cm margins, 12-point Arial or Times New Roman, 1.5 body spacing, no source code in the report, and an 8 to 12 page PDF user manual.
- Original allocation: reports/cycle3_master_plan.md and cycle3_task_packs/07-ch6-testing-yang-mingjie.md.
- Functional and quality baselines: original task pack 02 and final_report/ch02_zhang_zijian/draft.md. Conflicts are recorded in requirement_crosswalk.md.
- Implementation evidence: backend/app/routers/, models/, services/, data/ and frontend/. Existing tests are referenced individually by the full case CSV and source hashes.
- Benchmark: graphrag（终）/final_systematic_report.csv. Full precision is retained in the evidence CSV.
- Evaluator inspection: graphrag（终）/systematic_eval_engine.py and ragas_evaluator.py. The latter is not a RAGAS metric implementation. No credential values are reproduced.
- Existing architecture statements reviewed against code: current Ch4 draft and original Ch4.6 draft. Findings appear in peer_review.md.

## New observations on existing software

- Captured pytest summaries and JUnit XML for both snapshots; unchanged original tests.
- AST test-function inventory and SHA256 hashes, stored in audit.json.
- Loopback HTTP observations and 100 samples per existing operation in http_measurements.json.
- Actual browser walkthrough and strict offline first load, in browser_probe.json and screenshots/.
- Five academic or standards references are listed at the end of draft.md. The sources support methods and terminology, not invented project measurements.

The new observations are not new product capabilities or new benchmark results. Proposed improvements are explicitly identified as future work. Historical bug counts, novice user results, cloud latency, RAGAS scores and a 4,445-item evaluated sample are not asserted.

## Live GitHub recheck on 29 October 2026

- Latest master: 7d29bad88dd6db78bbab76ab9295d2eab246b6e1. GitHub's tree and comparison APIs were read again; evidence/github_recheck.json records the checked paths and hashes.
- All 296 original files were compared with current Git blob hashes. Only backend/run.py changed, adding the repository root to the import path for direct startup. All 12 test source files (including configuration and package initialisation), application modules, frontend and requirements remain identical to the tested ae7ab47 snapshot.
- Task packs 07/02, the master plan, official brief, later Chapter 2 draft, original MMLU CSV and both evaluator sources remain identical. The delivered CSV was checked byte-for-byte against the repository source; its macro gain remains +0.604005 percentage points.
- The former sync/cycle3-final branch is absent; master and submit-in-this-branch are available. develop is absent, so the group lead must confirm the receiving branch. Historical test records retain their actual commit identifiers and durations.
- Newly added reports/test_plan.md contains eight group-authored scenarios. Its statuses are not independent observations by this contributor and are not added to the 183-case result. A new group software ZIP and added chapter files are separate artefacts; their existence does not establish that a new package passed acceptance.
- The group software ZIP was separately downloaded and checked against its current GitHub blob hash. Its archive is valid, but it lacks eight current auth/report source/test files and differs in twelve other application/test files. It was inspected, not executed. The manual identifies this mismatch and applies to the tested source rather than that different package. No credential values or package contents are copied into the report bundle.

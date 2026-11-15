# Owner understanding notes

These are study notes, not a record of an oral assessment.

## Short explanation

The assigned review checks that requirements, implementation and reported evidence agree. The review follows a fixed repository snapshot. The existing suite passed 232 tests, and an additional check matched all 68 option responses to the authored answers and traps. The parser accepted the valid sample and rejected the invalid sample.

The main limitations are that the public quiz endpoint reveals answers, report statistics are fixed rather than updated by these submissions, and several report contracts differ from the code. The content-audit script also fills human-review labels automatically, so it cannot establish independent subject accuracy. The online baseline script is incomplete. These findings are recorded with evidence and suggested corrections.

Use the files and raw results to prepare the required explanation and demonstration.

## Questions to understand

1. What does 68/68 prove? It shows that the code agrees with the same bank's stored mappings. It does not prove that the authored answers are academically correct or that students learn better.
2. Why keep LY and ZZ prefixes? Some original IDs have different meanings in different source sections. The prefixes keep the source clear without claiming to renumber team requirements.
3. Why can all tests pass while requirements fail? Existing tests may check response shape and robustness without checking answer privacy, dynamic telemetry or the stated HTTP contract.
4. What was timed? Ten warmups then 100 serial in-process TestClient calls. These timings exclude browser and real network latency.
5. Is diagnosis fully offline? This local run used no model credentials. With credentials and guidance enabled, an optional model branch is reachable. Complete air-gapped browser behaviour was not tested.
6. What should happen next? The team should decide intended contracts, fix or qualify claims, add relevant acceptance checks and record real source review. The explanation should cover the evidence and one unresolved limitation in English.

## Five-minute walkthrough

Open traceability_update.md and explain one requirement row. Open review_results.json and locate quiz.public_answer_fields, option_checks and telemetry. Read F02 and F04 in review_log.md. Run run_review.py in the documented environment. Explain why exit 0 does not resolve the open gaps. Record UNDERSTOOD only after an actual explanation and demonstration.

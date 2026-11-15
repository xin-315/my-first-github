# Cycle 4 traceability update

## Basis and notation

Reviewed on 9 November 2026 at baseline `5687727e903311a081896208e800e1d0f6c322cf`.

This supplements `reports/rtm.md` and the earlier Chapter 3 Appendix B. LY and ZZ are author-qualified review row keys identifying the two preserved sections of `reports/rtm.md`; they are not new requirement IDs. The original FR/NFR identifiers and eight-use-case meanings are retained. The six-use-case numbering in the current Chapter 3 draft has different meanings and must not be substituted silently.

Status: PARTIAL means some specified behaviour is evidenced; GAP means a criterion is contradicted or the specified contract is absent; UNVERIFIED means evidence is insufficient for acceptance. No full requirement is signed off solely because the regression suite passes.

Paths in the implementation column are under `backend/app/` unless explicitly qualified. Original JSON evidence is `evidence/review_results.json`; the 15 November rerun is `evidence/2026-11-15/review_results.json`. Named test files are under `tests/` and ran as part of the full suite.

## Inherited requirement coverage

| Review row | Original ID | Original UC | Requirement | Implementation | Evidence | Status | Limit or discrepancy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| LY-FR-01 | FR-01 | UC-02 | Select a study domain | routers/quiz.py; services/quiz_service.py | review_results.json: quiz; test_quiz.py | PARTIAL | subject=law returns 3; category=law is ignored and returns 17. Browser selection untested. |
| LY-FR-02 | FR-02 | UC-01, UC-02 | Submit one answer per on-screen attempt | routers/diagnose.py; models/diagnose.py | option_checks; boundary_checks | GAP | Valid submissions work; answer protection fails. One-attempt UI locking was not tested; /api/answer is an older contract. |
| LY-FR-03 | FR-03 | UC-01 | Identify misconception and missing prerequisite | services/diagnostic_service.py; data/seed_questions.py | option_checks: all 51 distractors | PARTIAL | All authored trap IDs, descriptions and prerequisites match; independent content correctness remains unverified. |
| LY-FR-05 | FR-05 | UC-03 | Inspect evidence, source and review status | models/quiz.py; frontend/app.js | source inspection | GAP | QuizItem has no structured source/evidence/review_status contract. Inline source mentions do not establish formal verification. |
| LY-FR-06 | FR-06 | UC-04 | Inspect question-specific knowledge subgraph | models/quiz.py; frontend/app.js: renderGraph | source inspection | UNVERIFIED | Graph structures/rendering exist; graph interaction and keyboard acceptance require browser checks. This is not GraphRAG retrieval. |
| LY-NFR-01 | NFR-01 | UC-01, UC-02 | Secure API and credential handling | routers/quiz.py; models/quiz.py | quiz.public_answer_fields; public_option_fields | GAP | Unauthenticated response contains answer, explanation, traps and correctness flags. Full credential audit not performed. |
| LY-NFR-02 | NFR-02 | UC-01, UC-02 | Local reliability without cloud dependency | main.py; diagnostic_service.py; frontend/index.html | static_root_status; option_checks; pytest.txt | PARTIAL | Local in-process API works without model credentials. Complete air-gapped browser operation untested; ECharts is loaded from a CDN. |
| LY-NFR-03 | NFR-03 | UC-01, UC-03, UC-04 | Transparent diagnosis and provenance | diagnostic_service.py; models/quiz.py | option_checks; quiz model inspection | PARTIAL | Misconception/prerequisite mapping works; formal evidence and review-status traceability remains absent. |
| LY-NFR-04 | NFR-04 | UC-02, UC-04 | Keyboard accessibility | frontend/app.js; frontend/index.html | no browser run | UNVERIFIED | Source and static-serving tests cannot establish focus order, activation or screen-reader support. |
| LY-NFR-05 | NFR-05 | UC-02, UC-04 | Responsive layout | frontend/style.css | no viewport run | UNVERIFIED | 390px/1440px acceptance has not been executed. |
| LY-NFR-06 | NFR-06 | UC-03 | Reproducible provenance and evaluation | scripts/audit_online_baseline.py; audit_hallucination_l1_l3.py | audit_method; review_log F06/F07 | GAP | Review protocol is reproducible; held-out live comparison and formal content provenance are not demonstrated. |
| LY-NFR-07 | NFR-07 | UC-01, UC-02 | Local API performance | routers/diagnose.py | timing: 100 samples after 10 warmups | PARTIAL | Measured in-process latency only; does not establish TCP response time or startup SLA. |
| LY-NFR-08 | NFR-08 | UC-01 to UC-04 | Modular organisation | backend/app/routers; backend/app/services; frontend | pytest.txt; dependency snapshot | PARTIAL | Modular structure and local suite run verified; full clean deployment package not assessed. |
| ZZ-FR-04 | FR-04 | UC-05 | Five-dimension mastery analysis | services/report_service.py; frontend/app.js | telemetry before/after | GAP | Report statistics unchanged after three attempts; correct-rate-by-dimension and insufficient-evidence threshold not established. |
| ZZ-FR-05 | FR-05 | UC-08 | Socratic guided follow-up | diagnostic_service.py; frontend/app.js | optional_llm_path; test_diagnose.py | PARTIAL | Diagnosis guidance/fallback is covered; free-text tutoring quality and UI failure recovery not exercised. |
| ZZ-FR-06 | FR-06 | UC-07 | Same-knowledge-point supplementary recommendation | source inspection; OpenAPI routes | routes; existing appendix findings | UNVERIFIED | No end-to-end recommendation acceptance evidence; static recommendations are not an adaptive selection workflow. |
| ZZ-FR-07 | FR-07 | UC-06 | Search, filter and retry wrong-answer history | frontend/app.js | source inspection; no browser run | UNVERIFIED | No demonstrated persistent attempt archive, filter or retry workflow. |
| ZZ-FR-08 | FR-08 | UC-05, UC-07, UC-08 | Traceable question evidence and review status | models/quiz.py | source inspection | GAP | No structured provenance/review-status fields in current public quiz contract. |
| ZZ-FR-09 | FR-09 | UC-05, UC-08 | Hints and requested explanations | routers/quiz.py; diagnostic_service.py | quiz.public_answer_fields | GAP | Full answer/explanation is available before an attempt; request-only disclosure cannot be claimed. |
| ZZ-FR-10 | FR-10 | UC-05, UC-06, UC-07 | Save, read and clear learning records | frontend/app.js; report_service.py | telemetry; no persistence browser run | UNVERIFIED | Settings/profile storage is not evidence of persistent attempts and confirmed deletion. |
| ZZ-NFR-02 | NFR-02 | UC-05 to UC-08 | External-model failure fallback | diagnostic_service.py | test_diagnose_resilience_under_mocked_network_outage; option_checks | PARTIAL | Backend diagnosis fallback works in tested conditions; tutor-chat recovery is a separate untested workflow. |
| ZZ-NFR-03 | NFR-03 | UC-05 to UC-08 | Usability and accessibility | frontend/app.js; frontend/style.css | source inspection | UNVERIFIED | Theme/labels exist; complete accessibility audit not executed. |
| ZZ-NFR-04 | NFR-04 | UC-05 to UC-08 | Record privacy and answer protection | routers/quiz.py; models/quiz.py | quiz.public_answer_fields | GAP | Pre-attempt answer disclosure confirmed; attempt deletion has not been validated. |
| ZZ-NFR-07 | NFR-07 | UC-05, UC-07, UC-08 | Clear explanations without overstating results | services/report_service.py | telemetry; review_log F04 | GAP | Static values are labelled session_telemetry. Insufficient-evidence display is unverified. |
| ZZ-NFR-08 | NFR-08 | UC-05 to UC-08 | Mobile and desktop support | frontend/style.css | no browser run | UNVERIFIED | Responsive CSS is present; usable target widths require actual viewport checks. |

## Bounded Cycle 4 slice

These are review check IDs, not replacement requirement IDs. The independently reviewed slice is the implemented JSON-pack parser and its hand-off to the existing diagnosis service; no new retrieval/dashboard feature is assumed complete.

| Check | Requirement link | Criterion | Result and evidence |
| --- | --- | --- | --- |
| C4-01 | LY-FR-03 | Published valid pack produces accepted models | 2 accepted, 0 errors/warnings; parser.valid_pack.json |
| C4-02 | LY-NFR-08, robustness contribution | Published invalid pack is rejected with actionable issues | 12 errors, 1 warning, CLI exit 1; parser.invalid_pack.json |
| C4-03 | LY-FR-03 | Parsed pack feeds diagnosis without replacing the global bank | `tests/test_question_parser.py::test_diagnosis_runs_on_a_parsed_pack` passed |
| C4-04 | LY-FR-01 | Subject vocabulary covers shipped content | 9 subjects; `test_known_subjects_cover_the_seed_bank` passed |
| C4-05 | LY-FR-03, LY-NFR-03 | Every shipped wrong option resolves to its authored misconception/prerequisite | 51/51 distractors match; option_checks |
| C4-06 | LY-NFR-06 | Evidence is rerunnable and limitations are explicit | run_review.py, evaluation_procedure.md, dependency snapshot and raw observations |

The parser is demonstrated through the authoring CLI and direct service injection. This review does not establish an upload API, integration of newly parsed packs into the running frontend, or dynamic quiz generation.

## R01-R14 alignment warning

The `requirement_crosswalk.md` in the parent folder is provisional and conflicts with the current Chapter 2 table. For this reviewed snapshot, Chapter 2 defines R10 as the optional online baseline hook, R12 as exclusion of live LLM generation on the critical path, R13 as exclusion of runtime crowdsourcing, and R14 as exclusion of native apps/push scheduling. The older crosswalk gives these IDs other meanings. Both the numbering and requirement wording need owner agreement before final report integration. See F08 and F09; no canonical renumbering is asserted here.

## Current Chapter 2 R01-R14 review

These labels refer specifically to `reports/final_report/ch02_zhang_zijian/draft.md` at the baseline. They do not resolve the conflicting numbering in other sources.

| ID | Chapter 2 meaning | Review result | Evidence / limitation |
| --- | --- | --- | --- |
| R01 | Question bank filtering | PARTIAL | subject filtering works; category parameter and 12-item total are stale (F01) |
| R02 | Selection and submission | PARTIAL | All 68 authored options match; invalid-input HTTP contract differs (F03) |
| R03 | Option-level trap diagnosis | PARTIAL | 51 distractors match exact stored mappings; response uses flat fields rather than the documented nested trap/graph contract |
| R04 | Five-dimensional competency radar | GAP | Static report data; exact requested summary schema and dynamic profile not demonstrated (F04) |
| R05 | Session telemetry and reset | GAP | No change after three attempts; no reset API in OpenAPI (F04) |
| R06 | Local authentication/identity context | PARTIAL | Existing auth tests pass; OpenAPI exposes demo-users/login/register, but no auth/me or auth/logout endpoints required by Chapter 2 |
| R07 | Runtime bilingual UI and payload | PARTIAL | Frontend has bilingual content; QuizItem lacks the stated *_en API fields. No browser language-switch timing run (F09) |
| R08 | Dual-theme visual ergonomics | UNVERIFIED | Theme source exists; WCAG contrast and flicker-free persistence not measured |
| R09 | Entire application offline/single process | PARTIAL | Local static mount and tests work; physical network-isolation, cold-cache CDN behaviour and startup threshold unverified (F10) |
| R10 | Optional online baseline hook | PARTIAL | No-key skip path exists; actual live comparison is a placeholder (F07) |
| R11 | Exclude multi-tenant instructor management | UNVERIFIED | No corresponding route in current OpenAPI; a complete dead-button/packaging audit was not performed |
| R12 | Exclude live cloud generation on critical path | GAP | Mock provider called once when key/guidance enabled; zero-call exclusion contradicted (F05) |
| R13 | Exclude runtime question crowdsourcing | PARTIAL | No upload route in OpenAPI; authoring CLI is separate. Full runtime mutation/security audit unperformed |
| R14 | Exclude native mobile/push scheduling | UNVERIFIED | No native app or scheduler was demonstrated in this review; full release packaging audit outside scope |

A PARTIAL result against an excluded feature means limited inspection supports its exclusion, not that the feature is partly implemented.

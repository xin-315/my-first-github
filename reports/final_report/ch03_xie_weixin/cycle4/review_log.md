# Independent claims review log

Reviewed baseline: `5687727e903311a081896208e800e1d0f6c322cf`; date: 9 November 2026.

All findings are OPEN. Suggested owners identify roles for handover; they are not assignments accepted by those members. Severity reflects the effect on report credibility or acceptance. The findings below describe the reviewed implementation and supporting evidence. They do not constitute team acceptance or resolution of the identified issues.

## F01 — High

- Source: `reports/final_report/ch02_zhang_zijian/draft.md, R01; ch03_xie_weixin/draft.md, UC-01`
- Claim or criterion under review: The bank has 12 items and category filters the quiz.
- Evidence: quiz.all_count=17; category_law_count=17; subject_law_count=3; bank.traps=51.
- Proposed correction/action: The reviewed runtime contains 17 questions in 9 subjects and 51 traps. Filter with subject=law. Clearly label any 12-question/four-subject historical subset.
- Follow-up: Requirements/report owners. Status: OPEN.

## F02 — High

- Source: `reports/rtm.md, LY FR-02/NFR-01 and ZZ NFR-04; backend/app/routers/quiz.py`
- Claim or criterion under review: Public questions must not disclose answer keys and hidden mappings.
- Evidence: quiz.public_answer_fields contains answer/explanation/traps; option fields contain correctness flags and trap links.
- Proposed correction/action: Public answer protection is not satisfied in this snapshot. Introduce a separate public schema and add a negative disclosure test before claiming completion.
- Follow-up: Backend and security/test owners. Status: OPEN.

## F03 — High

- Source: `reports/final_report/ch03_xie_weixin/draft.md, UC-02; ch02_zhang_zijian/draft.md, R02`
- Claim or criterion under review: Invalid question is 404; E/empty/lowercase inputs are rejected with 422.
- Evidence: boundary_checks: unknown ID, E, empty object and lowercase a each returned 200; lowercase a normalised to A.
- Proposed correction/action: The current service uses fallback responses for unknown questions and accepts unrecognised option strings. Decide the intended contract and align validation, documentation and tests. Do not imply fallback B is a valid answer for an unknown question.
- Follow-up: Backend and requirements owners. Status: OPEN.

## F04 — High

- Source: `reports/final_report/ch03_xie_weixin/draft.md, UC-04; ch02_zhang_zijian/draft.md, R04/R05; backend/app/services/report_service.py`
- Claim or criterion under review: Every submission updates report telemetry; reset clears it.
- Evidence: telemetry unchanged after three wrong attempts; source returns fixed counts/scores tagged session_telemetry; reset probe 405 and no OpenAPI reset route.
- Proposed correction/action: The current report API serves fixed demonstration statistics. This review does not demonstrate accumulation or reset. Label demonstration data accurately or implement and verify session storage.
- Follow-up: Backend/report owners. Status: OPEN.

## F05 — High

- Source: `reports/final_report/ch02_zhang_zijian/draft.md, R12; backend/app/services/diagnostic_service.py`
- Claim or criterion under review: There are zero external HTTP calls on the diagnosis path.
- Evidence: optional_llm_path records one mocked provider await with a synthetic key and include_socratic=true.
- Proposed correction/action: Without credentials, wrong-answer guidance uses the local seed. With credentials and guidance enabled, the service may call Qwen and fall back if it fails. No real provider performance was measured.
- Follow-up: Architecture and implementation owners. Status: OPEN.

## F06 — High

- Source: `scripts/audit_hallucination_l1_l3.py, run_l1_audit/run_l2_audit; reports/audit/verdict.json`
- Claim or criterion under review: Generated human-verdict columns support independent content and attribution review.
- Evidence: Source assigns human_verdict TRUE/CONSISTENT directly. L1 checks blank text; L2 fills consistency without independent judgement.
- Proposed correction/action: These generated tables contain structural checks and default labels. Independent subject review has not been established by the script; do not use its labels as proof of factual truth or human sign-off.
- Follow-up: Audit/report owners. Status: OPEN.

## F07 — High

- Source: `scripts/audit_online_baseline.py, main; reports/audit/verdict.json`
- Claim or criterion under review: A live baseline comparison is available once credentials are present.
- Evidence: No-key branch writes a skip record. Live branch only prints a message and contains a placeholder comment; no experiment loop or result writer.
- Proposed correction/action: The online comparison is not implemented in this script. A successful exit or skip is not an evaluated baseline and cannot establish a hallucination reduction.
- Follow-up: Evaluation owner. Status: OPEN.

## F08 — High

- Source: `reports/rtm.md; reports/final_report/ch03_xie_weixin/requirement_crosswalk.md; ch02_zhang_zijian/draft.md`
- Claim or criterion under review: FR/NFR/R and UC identifiers can be treated as one stable scheme.
- Evidence: RTM preserves two conflicting meanings; provisional crosswalk disagrees with Chapter 2 for R10/R12/R13/R14; Chapter 3 six UCs differ from RTM eight UCs.
- Proposed correction/action: Keep source-qualified IDs until the group agrees a canonical scheme. Map by meaning and acceptance criterion, never by number alone. Current traceability addendum preserves all 25 inherited rows.
- Follow-up: Requirements lead and report editor. Status: OPEN.

## F09 — Medium

- Source: `reports/final_report/ch02_zhang_zijian/draft.md, R07/R08; ch03_xie_weixin/draft.md`
- Claim or criterion under review: Described payload fields, filenames and named test classes match the code.
- Evidence: QuizItem lacks stem_en/title_en/desc_en; actual CSS is frontend/style.css; test_diagnose.py uses function tests rather than listed TestErrorHandling classes.
- Proposed correction/action: Anchor assertions to existing symbols and tests. Browser bilingual content is distinct from bilingual API fields; neither implies the other. No 16 ms language-switch timing was performed.
- Follow-up: Chapter owners. Status: OPEN.

## F10 — Medium

- Source: `reports/final_report/ch02_zhang_zijian/draft.md, R09; frontend/index.html`
- Claim or criterion under review: The entire browser application has zero external dependencies.
- Evidence: Local static root returned 200 and offline-key API checks passed; index.html loads ECharts 5.5.1 from fastly.jsdelivr.net.
- Proposed correction/action: The API works locally in this review. Full cold-cache air-gapped frontend operation remains unverified; vendor assets or demonstrate supported fallback before claiming it.
- Follow-up: Deployment and UI owners. Status: OPEN.

## F11 — Medium

- Source: `README.md; reports/final_report/ch02_zhang_zijian/draft.md, R09; reports/audit/verdict.json`
- Claim or criterion under review: 145/147 passing tests or 84/36/12 audit denominators describe the entire current baseline.
- Evidence: Current regression: 232 passed; bank: 17 questions/51 traps. Historical audit main selects law_/cs_/econ_/se_ prefixes and asserts 84/36/12.
- Proposed correction/action: State the commit and subset for each historical count. Use 232 for this executed suite; report 17/51 current totals. Do not expand historical audit conclusions to all 9 subjects.
- Follow-up: Testing/report owners. Status: OPEN.

## F12 — Medium

- Source: `reports/rtm.md, evidence/source/review-status rows; backend/app/models/quiz.py`
- Claim or criterion under review: Question evidence and formal review status are traceable fields.
- Evidence: Current QuizItem schema has no source, evidence or review_status field. Explanations may contain textual citations but no explicit review workflow was verified.
- Proposed correction/action: A citation-like explanation is not a verified source record. Record structured provenance and actual independent review before claiming formal content verification.
- Follow-up: Content and requirements owners. Status: OPEN.

## Verified positive findings

- All 232 existing tests passed in the recorded environment; this is stronger evidence than inspecting test files alone, but only for their actual assertions.
- All 68 shipped option responses agreed with the stored answer/trap mappings. This includes exact misconception/prerequisite checks for all 51 distractors.
- The two published parser samples behaved as expected. The existing suite also passed the parser-to-diagnosis integration test and seed-bank round-trip.
- Subject filtering with the documented runtime parameter `subject` worked in the reviewed examples.

## Decision and follow-up order

First resolve the public answer-disclosure contract, invalid-input behaviour and static telemetry claims. Then agree identifiers and correct stale report passages. Treat content audit and live baseline results as unverified until genuine source review and controlled measurement exist. Schedule browser/accessibility/deployment checks separately. Re-run the relevant checks after product changes and update the baseline commit.

The review does not change product code or silently redefine an acceptance criterion to match the implementation. Suggested replacement wording describes the observed implementation; the original target remains a gap unless the team explicitly revises it.

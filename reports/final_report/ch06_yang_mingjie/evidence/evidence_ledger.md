# Evidence ledger

All observations refer to existing Cycle 3 commit ae7ab47c6ff77b17f0ca62836b2c01e36da57187 unless explicitly labelled master. Original application and test files were not modified.

| Key | Evidence and interpretation |
| --- | --- |
| T01 | Assigned R01: subject filtering and existing browser checks demonstrate all four original disciplines. See F01 for the stricter later-draft criterion. |
| T02 | Assigned R02: the recorded browser option selection produces a diagnosis verdict and HTTP 200. |
| T03 | Assigned R03: option-specific feedback exists, but its field names differ from title/desc/prereq/radar_hit; partial. |
| T04 | Assigned R04: five dimensions are returned; trend values are fixed, limiting the title's implied progression; partial. |
| T05 | Assigned R05: summary metrics and unknown-subject empty state exist, but an actual zero-attempt learner state is not represented; partial. |
| T06 | Assigned R06: demonstration login/register return sessions, but duplicate registration is 200 rather than the specified 409; partial. |
| T07 | Assigned R07: an in-page switch to English is recorded, without navigation/reload. This assesses interface switching, not every translation. |
| T08 | Assigned R08: the theme changes, but complete AA contrast remains unverified; partial. |
| T09 | Assigned R09: static files require no Node build, but fresh offline browser loading fails on ECharts; unmet. |
| T10 | Assigned R10: all twelve stored graph-assisted benchmark rows are reported. No fresh engine rerun or online GraphRAG integration is demonstrated; partial. |
| T11 | Assigned R11 excludes multi-user/tenant isolation. This is a scope exclusion, not secure isolation evidence. |
| T12 | Assigned R12 excludes a native mobile app. It must not be confused with the later draft's cloud-call exclusion. |
| T13 | Assigned R13 excludes ranking/sharing. It must not be confused with the later draft's crowdsourcing exclusion. |
| T14 | Assigned R14 excludes adaptive exam assembly. It must not be confused with the later draft's native-mobile exclusion. |
| F01 | `cycle3/audit.json`: 17 seed questions, nine subject codes. `http_measurements.json`: subject=law returns 3; category=law returns 17. The draft's exact 12-question/category acceptance criterion is unmet. |
| F02 | `browser_probe.json`: selecting an existing option sends POST /api/diagnose and returns 200. `cycle3/audit.json`: unknown ID, Z and empty object return 200 fallback; type confusion returns 422. Strict draft error contract differs. |
| F03 | `cycle3/audit.json` diagnosis response contains trap_name, misconception, prerequisite and radar_dimension, not the draft's nested trap and graph object. Existing option-level tests pass; exact payload acceptance differs. |
| F04 | Five dimensions and scores are returned by /api/reports/trend. Existing report tests pass. `http_measurements.json` plus report_service.py show fixed metrics; summary schema differs from draft radar_scores expectation. |
| F05 | `http_measurements.json`: before and after a wrong answer, summary remains 18 attempts / 14 correct. POST /api/reports/reset returns 405. |
| F06 | Existing auth service ignores supplied passwords and synthesises predictable session strings. Wrong-password login returns 200; duplicate registrations return 200 twice. /api/auth/me returns 404; logout returns 405. No secure session claim is supported. |
| F07 | `browser_probe.json` records an in-page switch to en. Full payload translation and the draft's 16 ms requirement have not been established. |
| F08 | `browser_probe.json` records a switch to light; preference is stored by the existing script. No complete AA contrast audit was performed, including gradients and selected/disabled states. |
| F09 | `browser_probe.json`: strict fresh offline load raises echarts is not defined and creates zero option cards. API-only pytest remains offline-capable. |
| F10 | Existing scripts/audit_online_baseline.py has a no-key skip path. Its live branch is a placeholder. Existing GraphRAG CSV is research evidence only; online UI integration is not demonstrated. See online_baseline_skip.txt. |
| F11 | No instructor management routes in captured OpenAPI. Exclusion is scoped; no assertion of secure tenant isolation. |
| F12 | diagnostic_service.py retains an optional key-enabled external call. Therefore the draft's absolute ban on network work in this path is not enforced. Tests used no live credentials. |
| F13 | Captured routes contain no question-upload or trap-edit endpoint. The existing bank is curated and read-only through these APIs. |
| F14 | No native mobile client or push scheduling service is delivered by the inspected software. This is a scope exclusion, not an implemented feature. |
| N01 | Loopback diagnosis P95 1.128 ms, 100 observations after five warm-ups. This is not the requested 1,000-call in-process concurrent measurement; full draft criterion remains unverified. |
| N02 | Startup was observed successfully, but no controlled cold-start time was captured. Do not reuse the draft's 0.65 s. |
| N03 | API regression passes with external sockets rejected. Fresh-browser full offline availability fails; see F09. |
| N04 | Original adversarial suite 38/38 passes under its permissive contracts. Strict 404/422 expectation fails for selected fallback cases. |
| N05 | Tested option selection opens a drawer directly. No novice user study, full five-layer timing or reproducible under-five-second acceptance measurement was conducted. |
| N06 | Theme toggle is demonstrated. Full contrast across all states remains unverified; screenshot alone is not a contrast measurement. |
| N07 | Existing alias tests pass, including auth, quiz and reports. This supports tested field compatibility, not the draft's universal zero-undefined guarantee. |
| N08 | Static frontend has no required Node build. Frontend and backend maintain separate seed/configuration data; automatic propagation of every added discipline is not demonstrated. |
| N09 | Hardcoded credential configuration was located in existing frontend/research files. Credential values are deliberately absent here. Auth service does not implement the draft's salted password hashing. |
| N10 | Report service returns constants labelled session_telemetry. That label does not establish actual attempt aggregation. Existing narrative and audit-script claims require separate verification. |

## Measurement conditions

Browser captures are at 1440 by 1000 in headless Edge. The functional run fulfils the existing CDN request with the exact downloaded ECharts 5.5.1 file, SHA256 e84270bd0cd5bdf60fefc26d00c2a391cb2e81f4d26a7a9ee16185a54773a3cf. This is a QA fixture and is not bundled in the application. Other remote requests, including model calls, were blocked. The independent fresh offline run had no vendor fixture.

The case CSV lists all 183 collected cases; JUnit XML supplies outcomes and timings. Browser and HTTP observations are supplementary probes, not additional pytest cases. The original run-summary image is labelled as a captured-transcript view. A separate live local console capture and its rerun evidence are identified independently; neither claims to be an operating-system terminal screenshot.

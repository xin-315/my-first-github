# Requirement baseline crosswalk

This personal contribution follows task pack 07 by using assigned task pack 02 Table 2.2 as the main functional baseline. The main table and the table below quote its Chinese labels verbatim after removing Markdown bold markers; English translations follow below. The later Ch2 draft calls its functional matrix Table 2.1 and its quality matrix Table 2.2, with changed definitions. That later draft is assessed separately rather than silently substituted.

| ID | Original task requirement | Original priority | Current Ch2 title | Current priority | Assessment against original task |
| --- | --- | --- | --- | --- | --- |
| R01 | 学生可按学科浏览题目 | Must | Multi-Disciplinary Question Bank Filtering | Must | Met for original four subjects with subject filtering; current bank has 17 questions. |
| R02 | 学生可提交作答 | Must | Interactive Option Selection & Attempt Submission | Must | Met for selecting an existing option and receiving a verdict. |
| R03 | 系统提供选项级诊断（非题目级） | Must | Option-Level Misconception & Trap Diagnosis | Must | Partial: option diagnosis exists, but exact four-field response schema differs. |
| R04 | 五维能力雷达与趋势 | Must | Five-Dimensional Competency Radar Profiling | Must | Partial: five scores exist, but backend trend is a fixed demonstration baseline. |
| R05 | 学情摘要卡 | Must | Session Telemetry, Trend & Weakness Aggregation | Must | Partial: summary and unknown-subject empty state exist, but zero-attempt real-user state is not modelled. |
| R06 | 登录与注册 | Must | Local Session Authentication & Identity Context | Should | Partial: login/register demonstration exists; duplicate 409 is not implemented. |
| R07 | 中英双语界面 | Should | Runtime Bilingual Interface & Payload Support (zh / en) | Should | Met for the assigned interface-switching criterion: runtime switching observed without reload. Full translation coverage is not claimed. |
| R08 | 明/暗双主题 | Should | Dual-Theme Visual Ergonomics (Cyber Obsidian / Academic Daylight) | Should | Partial: both themes toggle; complete AA contrast remains unverified. |
| R09 | 离线零构建运行 | Must | 100% Offline Single-Process Execution | Must | Unmet for fresh offline browser loading due to external ECharts dependency. |
| R10 | GraphRAG 图谱增强 | Should | Optional Online LLM Baseline Audit Hook | Could | Partial: stored graph-assisted benchmark exists; no verified online GraphRAG integration or new benchmark rerun. |
| R11 | 多用户/多租户隔离 | Won't | Multi-Tenant Instructor Dashboard & Roster Management | Won't | Excluded by scope; no tenant isolation claim. |
| R12 | 移动原生 App | Won't | Real-Time Live Cloud LLM Generation on Critical Path | Won't | Native app excluded. Current draft R12 instead concerns cloud calls, which are conditionally present. |
| R13 | 社交功能（排行榜/分享） | Won't | Unmoderated User-Generated Question & Trap Crowdsourcing | Won't | Social functions excluded. Current draft R13 instead concerns crowdsourcing. |
| R14 | 自动组卷 / 自适应出题 | Won't | Native Mobile (iOS/Android) Client & Push Spaced-Repetition Scheduler | Won't | Adaptive exam assembly excluded. Current draft R14 instead concerns native apps and push scheduling. |

## English translations of the assigned labels

**Translations of main Table 6.5 labels**

| ID | Priority | English translation | Result | Evidence |
| --- | --- | --- | --- | --- |
| R01 | Must | Browse questions by subject | Met | T01 |
| R02 | Must | Submit an answer | Met | T02 |
| R03 | Must | Option-level diagnosis | Partial | T03 |
| R04 | Must | Five-axis radar and trend | Partial | T04 |
| R05 | Must | Learning summary card | Partial | T05 |
| R06 | Must | Login and registration | Partial | T06 |
| R07 | Should | Chinese / English interface | Met | T07 |
| R08 | Should | Light / dark themes | Partial | T08 |
| R09 | Must | Offline, zero-build operation | Unmet | T09 |
| R10 | Should | GraphRAG enhancement | Partial | T10 |
| R11 | Won't | Multi-user / tenant isolation | Excluded | T11 |
| R12 | Won't | Native mobile application | Excluded | T12 |
| R13 | Won't | Social ranking / sharing | Excluded | T13 |
| R14 | Won't | Adaptive exam assembly | Excluded | T14 |

Translations only; the original wording is authoritative for this contribution.

## Original quality requirements

| Original ID | Original threshold | Assessment and evidence |
| --- | --- | --- |
| NFR-U1 | Unaided first-time answer; no more than three clicks | Partial: tester walkthrough only; novice acceptance not performed. |
| NFR-U2 | Bilingual and dual theme; contrast at least 4.5 to 1 | Partial: toggles verified; full contrast not verified. |
| NFR-P1 | Every API P95 below 100 ms locally without concurrency | Met in this observation: all nine route P95 values below 1.5 ms; no live model key. |
| NFR-P2 | First contentful paint below 100 ms | Unmet in this browser observation: 392 ms with the vendor fixture. |
| NFR-R1 | Demonstration has no external service dependency | Partial for APIs, unmet for fresh browser load. |
| NFR-R2 | Invalid inputs use classified errors and never 500 | Partial: no-crash tests pass, but several invalid inputs return 200 fallback. |
| NFR-S1 | Pydantic input validation; no SQL or command concatenation surface | Partial: typed inputs checked; unrestricted strings and frontend HTML handling prevent a universal security claim. |
| NFR-S2 | No plaintext credentials in repository or ZIP | Unmet in original application material; report package excludes credential values. |
| NFR-M1 | Layered modules and independently testable services | Layering exists; complete independent service isolation has not been measured. |
| NFR-M2 | At least 140 cases, all green, under 10 seconds | Met: 183 passed in 1.83 s; wall time 2.643 s. |

## Later Chapter 2 functional assessment

**Later-draft functional assessment, separate baseline**

| ID | Prio | Later Ch2 exact title | Result | Evidence |
| --- | --- | --- | --- | --- |
| R01 | Must | Multi-Disciplinary Question Bank Filtering | Partial | F01 |
| R02 | Must | Interactive Option Selection & Attempt Submission | Partial | F02 |
| R03 | Must | Option-Level Misconception & Trap Diagnosis | Partial | F03 |
| R04 | Must | Five-Dimensional Competency Radar Profiling | Partial | F04 |
| R05 | Must | Session Telemetry, Trend & Weakness Aggregation | Unmet | F05 |
| R06 | Should | Local Session Authentication & Identity Context | Partial | F06 |
| R07 | Should | Runtime Bilingual Interface & Payload Support (zh / en) | Partial | F07 |
| R08 | Should | Dual-Theme Visual Ergonomics (Cyber Obsidian / Academic Daylight) | Partial | F08 |
| R09 | Must | 100% Offline Single-Process Execution | Unmet | F09 |
| R10 | Could | Optional Online LLM Baseline Audit Hook | Partial | F10 |
| R11 | Won't | Multi-Tenant Instructor Dashboard & Roster Management | Excluded | F11 |
| R12 | Won't | Real-Time Live Cloud LLM Generation on Critical Path | Not enforced | F12 |
| R13 | Won't | Unmoderated User-Generated Question & Trap Crowdsourcing | Excluded | F13 |
| R14 | Won't | Native Mobile (iOS/Android) Client & Push Spaced-Repetition Scheduler | Excluded | F14 |

F keys resolve to evidence/evidence_ledger.md. These are not the assigned T-key requirements.

## Current Chapter 2 quality requirements

**Supplementary current Chapter 2 quality requirement mapping**

| ID | Current Chapter 2 quality attribute | Result | Evidence |
| --- | --- | --- | --- |
| NFR-01 | Diagnostic API Response Latency | Partial | N01 |
| NFR-02 | Application Cold-Start Time | Unverified | N02 |
| NFR-03 | Zero-Network Offline Determinism | Unmet | N03 |
| NFR-04 | Graceful Input Validation & Fault Isolation | Partial | N04 |
| NFR-05 | Diagnostic Interaction Efficiency (3-Click Rule) | Partial | N05 |
| NFR-06 | Visual Contrast & Dual-Theme Readability | Unverified | N06 |
| NFR-07 | Cross-Language Naming Contract (CamelModel) | Partial | N07 |
| NFR-08 | Zero-Build Frontend & Data-Code Separation | Partial | N08 |
| NFR-09 | Credential Hygiene & Zero-Secret Repository | Unmet | N09 |
| NFR-10 | Anti-Hallucination & Provenance Transparency | Unmet | N10 |

Source: current Ch2 Table 2.2 and evidence/evidence_ledger.md. The separate crosswalk evaluates all original NFR-U1 to NFR-M2 identifiers.

The personal contribution has one explicit assigned baseline. Any later group-wide change to that baseline is an integration decision for the report owners; it does not require this contributor to rewrite other members' chapters.

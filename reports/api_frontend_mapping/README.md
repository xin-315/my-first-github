# `api_frontend_mapping/` — Deliverable 2 Source Files & Export Specifications

**Lead Author**: Zixuan Liang (50106037, Task Rotation from Yusai Xi) | **Deliverable**: Phase 2 Kickoff Task Pack (2) Deliverable 2  
**Reviewers / Project Lead**: Yuxuan Wu (50106070, Project Manager) / Hao Jiang (50106065, Code Review Lead)  
**Target Technical Report Chapters**: Chapter 3 (Requirements Engineering), Chapter 4 (System Design and Architecture), Chapter 5 (Implementation)

---

## 1. Directory Contents

| File | Description |
| :--- | :--- |
| `api_frontend_mapping.md` | **Primary Deliverable**. Comprehensive Frontend–Backend Interface Mapping Specification: 4 live endpoints, field-level contracts, invariant constraints `C-01`–`C-03`, error and boundary handling matrices, 24 empirical test cases, 11 architectural gap analyses, `localStorage` schema, and academic abstract. |
| `api_frontend_mapping.mmd` | Service invocation architecture diagram source (Mermaid 11, strictly aligned with §2.2). |
| `api_frontend_mapping.svg` | Diagram export (Vector SVG, 1092×1219 units, embedded white background and 16-unit padding). |
| `api_frontend_mapping.png` | Diagram export (High-resolution PNG, 2248×2502 pixels, 2× scale). |
| `README.md` | This export and provenance documentation. |
| `_preview.html` | Visual fidelity check page (side-by-side SVG and PNG browser preview). |

*Preferred format for report insertion*: Please prioritise `.svg` for vector fidelity in Word/PDF documents.

---

## 2. Revisions Relative to Initial Task Brief

The baseline table provided in `02_architecture_task.md:99-104` originally reflected early conceptual prototypes. Through rigorous empirical probing against live running services, the following discrepancies were identified and systematically documented:

| # | Discrepancy / Observation | Impact | Resolution in Specification |
| :-: | :--- | :--- | :--- |
| 1 | Preset endpoints (`/api/quiz`, `/api/diagnose`, `/api/analytics/radar`, `/api/chat`) returned 404 in Phase 1 standalone prototype. | Discrepancy during manual integration. | Replaced with audited live endpoints; preset mappings reconciled in §8.1. |
| 2 | Theoretical assumption of external graph query / LLM synthesis in every call. | In Phase 1 prototype, answer evaluation is a deterministic local pure function. | System boundary accurately documented in §2.1 and §4.4. |
| 3 | Preset brief assumed query strings (`?subject=`, `?student_id=`). | Phase 1 prototype used strict `self.path` equality checks, failing on `?`. | Documented as Hard Invariant Constraint **C-03**; client-side filtering clarified. |
| 4 | Unconditional reading of `misconception` payload. | `app.js:283/287` reads without null guards; missing key causes `TypeError`. | Formulated as Invariant Constraint **C-01** with defensive recommendations. |
| 5 | Three-tier naming ambiguity of `misconceptions`. | Authoring object vs response object vs localStorage string. | Established Invariant Constraint **C-02** taxonomic disambiguation matrix. |
| 6 | Unhandled HTML error responses. | Successful responses are JSON; error responses default to Python `send_error()` HTML. | Documented in §6 Error Matrix and Appendix B verbatim captures. |
| 7 | Academic mastery radar endpoint assumed. | Radar and mastery statistics are client-side derivations from `localStorage`. | Documented derivation formula in §7; identified zero-endpoint client logic. |

---

## 3. Formatting and Sizing Recommendations for Technical Report

| Figure | Native Aspect Ratio | Recommended Layout | Notes |
| :--- | :--- | :--- | :--- |
| Interface Calling Diagram | 1092×1219 (~0.9:1) | **Portrait Page, Full Column (width 12–13 cm)** | Near square aspect ratio; renders clearly at 12–13 cm width with legible 12pt edge labels. |

---

## 4. Empirical Verification & Reproduction

All 24 empirical test cases with verbatim request payloads and response headers are fully preserved in Appendix B:

```powershell
py server.py                      # Run local service
py tools/benchmark_api.py --base-url http://127.0.0.1:8000 --iterations 20
```

---

## 5. Peer Review & Architecture Evolution Sign-Off

**Reviewers**: Yuxuan Wu (50106070, Project Manager), Hao Jiang (50106065, Code Review Lead) | **Date**: 2026-10-09

1. **Task Rotation Acknowledgement**: Formally confirmed that Deliverable 2 was undertaken, deepened, and empirically verified by Zixuan Liang (50106037) following task rotation from Yusai Xi.
2. **Academic Merit**: The 3 invariant constraints (`C-01`, `C-02`, `C-03`) and 11 architectural gap analyses (`G-01` to `G-11`) serve as essential empirical rationale for the Phase 2 FastAPI modular refactoring documented in Chapter 5.
3. **Traceability Closure**: The production `develop` branch has resolved all listed gaps via the modern FastAPI modular architecture (`backend/app/main.py`), Pydantic validation, and comprehensive automated test suite (114 passing tests).

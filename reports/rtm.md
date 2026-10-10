# StudyGraph — Combined Requirements Traceability Matrix (M2.1)

**Course:** JC2001 / Group 5  
**Project:** StudyGraph — Graph-Grounded Diagnostic Study Assistant  
**Compiled by:** Lin Yongtong (50106038), Requirements Lead  
**Contributors:** Lin Yongtong (50106038; UC-01–UC-04); Zhang Zijian (50106035; UC-05–UC-08)  
**Official project basis for this draft:** `docs/PROJECT_PROPOSAL_DRAFT.md`, Section 4  
**Status:** Compiled for group review; author definitions and pending items are deliberately retained  
**Internal deadline:** 10 October 2026, 22:00 (Asia/Shanghai)

## 1. Source precedence and traceability notation

The formal StudyGraph proposal defines five objectives:

| Objective | Meaning in the official StudyGraph proposal |
| --- | --- |
| Obj 1 | Runnable proof of concept: domain filtering, answer submission, misconception diagnosis, progressive help, evidence, graph and learning-history features |
| Obj 2 | At least 15 formally source-verified demonstration items, preserving source, evidence and review status |
| Obj 3 | Reproducible baseline-versus-evidence-assisted evaluation using fixed held-out items and the same model settings |
| Obj 4 | Traceable, modular, secure, accessible, responsive and reliably testable system |
| Obj 5 | Required JC2001 course deliverables by applicable deadlines, conditional on submission-arrangement confirmation |

**Two numbering systems currently coexist.** The original repository `docs/REQUIREMENTS_TRACEABILITY.md` uses FR-01–FR-08 and NFR-01–NFR-08. Zhang's PR #5 personal RTM uses FR-04–FR-10 and NFR-02/03/04/07/08 with some different meanings. As requested, no part of his table has been renamed or rewritten. We use author-qualified *row keys* (`LY-FR-05`, `ZZ-FR-05`) only in the explanatory integration index, while preserving each contributor's original ID in their own table. **These row keys are not replacement requirement IDs.** The final team should approve one canonical numbering scheme before signing off on the RTM, testing matrix or code traceability.

## 2. Requirement coverage index (author-qualified, no reinterpretation)

| Use case | Owner | Related requirements in owner's section | Notes |
| --- | --- | --- | --- |
| UC-01 | 50106038 | FR-02, FR-03; NFR-01, NFR-02, NFR-03 | Incorrect-answer diagnosis and local reliability |
| UC-02 | 50106038 | FR-01, FR-02; NFR-01, NFR-04, NFR-05 | Domain selection and one answer attempt |
| UC-03 | 50106038 | FR-05 (repository meaning: evidence), NFR-03, NFR-06 | Current question evidence; no cross-topic keyword graph search |
| UC-04 | 50106038 | FR-06 (repository meaning: graph), NFR-04, NFR-05 | Question-specific local knowledge map |
| UC-05 | 50106035 | See Zhang's unchanged personal RTM | Five-dimensional analysis |
| UC-06 | 50106035 | See Zhang's unchanged personal RTM | Historical incorrect answers |
| UC-07 | 50106035 | See Zhang's unchanged personal RTM | Adaptive recommendation (planned / not implemented) |
| UC-08 | 50106035 | See Zhang's unchanged personal RTM | Guided tutoring |

## Part A — Lin Yongtong's personal RTM (UC-01–UC-04)

The items below align with the source repository's requirement definitions. `Obj` is traced to the formal StudyGraph proposal, not to the former Neo4j/FastAPI project definition. "Current check" records the supplied project implementation and does **not** certify complete acceptance testing.

### A1. Functional requirements

| Original repository ID | Requirement (Lin scope) | Objective | Related use case | MoSCoW | Acceptance criterion | Current check |
| --- | --- | --- | --- | --- | --- | --- |
| **FR-01** | Select a study domain | Obj 1 | UC-02 | Must Have | The student can choose Computer Science, Software Engineering or All, and the visible question list matches the selection. | Browser filtering logic is present; full browser verification outstanding. |
| **FR-02** | Submit one answer per on-screen attempt | Obj 1, 4 | UC-01, UC-02 | Must Have | Public questions do not disclose the answer key; a valid selection invokes `POST /api/answer`, locks controls and records only an accepted attempt. | API handler and frontend state are present; boundary conditions require testing. |
| **FR-03** | Identify misconception and missing prerequisite | Obj 1, 2 | UC-01 | Must Have | An incorrect response has a named misconception and prerequisite; every curated incorrect option is structurally mapped. | Structural tests present; individual content source verification pending. |
| **FR-05** | Inspect evidence, source and content-review status (**repository meaning**) | Obj 1, 2 | UC-03 | Must Have | The current question displays its `evidence`, `source` and `review_status`; unreviewed items are not labelled formally verified. | Evidence UI exists; the six demo items remain `Source review pending`. |
| **FR-06** | Inspect question-specific knowledge subgraph (**repository meaning**) | Obj 1 | UC-04 | Should Have | Defined graph nodes and edges appear and clicking a node updates details. | Local JSON/SVG graph view exists; complete keyboard audit outstanding. |

### A2. Non-functional requirements

| Original repository ID | Requirement (Lin scope) | Objective | Related use case | MoSCoW | Acceptance criterion | Current check |
| --- | --- | --- | --- | --- | --- | --- |
| **NFR-01** | Secure API and credential handling | Obj 4 | UC-01, UC-02 | Must Have | `GET /api/questions` omits keys, explanation and misconception mapping; secrets do not appear in browser bundles or checked-in source. | Unit coverage for public-question filtering; full secret audit recommended. |
| **NFR-02** | Local reliability / no cloud dependency (**repository meaning**) | Obj 1, 4 | UC-01, UC-02 | Must Have | Core demonstration runs via local Python and JSON with no cloud credentials; errors are shown if the local server itself is inaccessible. | Local mode exists; clean-machine rerun outstanding. |
| **NFR-03** | Transparent diagnosis and provenance (**repository meaning**) | Obj 1, 2 | UC-01, UC-03, UC-04 | Must Have | Diagnosis states misconception/prerequisite, and evidence status is visible without claiming unreviewed materials are verified. | Data fields/UI implemented; independent source review pending. |
| **NFR-04** | Keyboard accessibility (**repository meaning**) | Obj 4 | UC-02, UC-04 | Should Have | Main controls and graph nodes support keyboard focus/activation and clear labels. | Partial UI support; complete accessibility audit outstanding. |
| **NFR-05** | Responsive layout | Obj 4 | UC-02, UC-04 | Should Have | Key controls are readable without horizontal overflow at 390px and 1440px widths. | Responsive styles and browser script supplied; verify on actual target browser. |
| **NFR-06** | Reproducible provenance and evaluation | Obj 2, 3, 4 | UC-03 (evidence linkage) | Must Have | Source IDs, content statuses and provenance persist; held-out evaluations keep item IDs/splits stable and outputs reproducible. | Scripts and metadata available; controlled comparison not completed. |
| **NFR-07** | Local performance (**repository meaning**) | Obj 4 | UC-01, UC-02 | Should Have | Local API median below 200ms on a documented machine according to repository baseline; report median and p95 separately. | Benchmark script provided; its p95 guard differs from median target. |
| **NFR-08** | Modular software organisation (**repository meaning**) | Obj 4 | UC-01–UC-04 | Should Have | User interface, service, curated data and test tools are separately maintained and startup steps are reproducible. | Separate modules and README supplied; code review ongoing. |

### A3. Acceptance-case IDs for Lin Yongtong

| Use case | Acceptance test IDs | Minimum planned evidence |
| --- | --- | --- |
| UC-01 | AT-01-01 to AT-01-05 | Unit/API check for non-exposed answer key and incorrect-answer diagnosis; UI failure branch |
| UC-02 | AT-02-01 to AT-02-05 | Domain selector, navigation, one-attempt submission and error handling |
| UC-03 | AT-03-01 to AT-03-04 | Evidence list, source and review status audit |
| UC-04 | AT-04-01 to AT-04-05 | Graph node selection, graph-edge validation and keyboard audit |

### A4. Author-specific status

| Use case | Implementation status (current project snapshot) |
| --- | --- |
| UC-01 | Local evaluation, diagnosis mapping and feedback exist; comprehensive error/storage testing outstanding. |
| UC-02 | Domain filtering and answer flow exist; complete end-to-end browser confirmation outstanding. |
| UC-03 | Evidence and review-status display exist; keyword graph search from earlier task brief is not implemented. |
| UC-04 | Local question-specific knowledge graph exists; live database traversal or free-text concept expansion is not part of this version. |

---

## Part B — Zhang Zijian's original personal RTM (50106035), reproduced without editing

**Archived source:** `sources/zhang_50106035_rtm_original.md`  
**Reference:** `https://github.com/xin-315/my-first-github/pull/5/files` (file `reports/add-use-cases-and-rtm-227/rtm.md`, snapshot commit `9413a58`).  
**Preservation note:** The original text below calls itself a *personal* RTM, refers to UC-01–UC-04 as not included in that personal submission, and asks Lin Yongtong to combine the two pieces. That original wording is preserved intentionally; this containing document is the combined review draft.

# StudyGraph Personal Requirements Traceability Matrix

**Owner:** 50106035 (Business Analysis)
**Personal scope:** UC-05, UC-06, UC-07 and UC-08
**Document status:** Personal section completed, pending merge review by 50106038
**Internal deadline:** 10 October 2026, 22:00 (Asia/Shanghai)

This matrix lists only the requirements related to the four use cases owned by
50106035. It is a personal RTM extract for 50106038 to merge into the complete
group RTM. It is not the final group-wide RTM.

## 1. Objectives

The objectives below follow Section 4 of `docs/PROJECT_PROPOSAL_DRAFT.md`:

| Objective | Description |
| --- | --- |
| Obj 1 | Deliver a runnable system supporting practice, diagnosis, hints, evidence, knowledge maps and learning history |
| Obj 2 | Prepare source-reviewed demonstration questions and retain evidence, sources and content status |
| Obj 4 | Demonstrate software quality through testing, security and responsive design |

## 2. Personal Functional Requirements

| Requirement ID (FR/NFR) | Requirement name and description | Related objective | Related use case | MoSCoW priority | Short acceptance criterion |
| :---: | --- | :---: | :---: | :---: | --- |
| **FR-04** | Five-dimension learning radar and mastery analysis | Obj 1 | UC-05 | **Should Have** | The radar can refresh after five valid attempts; it calculates a correct rate for each dimension; a dimension with fewer than two attempts shows “Insufficient evidence” |
| **FR-05** | Socratic guided follow-up | Obj 1, 2 | UC-08 | **Should Have** | A student question receives a 2-3 sentence response related to the current question, with a prompt or counter-question instead of the direct answer |
| **FR-06** | Same-knowledge-point variant or supplementary question recommendation | Obj 1 | UC-07 | **Could Have** | When a suitable question exists, the system recommends a different question for the same knowledge point and explains the reason; otherwise it gives a clear message |
| **FR-07** | Search, filter and retry historical wrong answers | Obj 1 | UC-06 | **Should Have** | Students can search by keyword, subject, topic, misconception or result; a retry creates a new record and does not overwrite the original |
| **FR-08** | Traceable question evidence, source and review status | Obj 1, 2 | UC-05, UC-07, UC-08 | **Must Have** | Questions show evidence, source and review status; pending content is not labelled as reviewed |
| **FR-09** | Hints and student-requested explanations | Obj 1 | UC-05, UC-08 | **Must Have** | Viewing a hint or explanation does not create an attempt; the full explanation is shown only after the student requests it |
| **FR-10** | Save, read and clear learning records | Obj 1 | UC-05, UC-06, UC-07 | **Must Have** | A successful attempt is saved once; it can be read after refresh; clearing requires confirmation and cancelling keeps the records |

## 3. Personal Non-Functional Requirements

| Requirement ID (FR/NFR) | Requirement name and description | Related objective | Related use case | MoSCoW priority | Short acceptance criterion |
| :---: | --- | :---: | :---: | :---: | :---: | --- |
| **NFR-02** | Fallback behaviour when an external model or service fails | Obj 1, 4 | UC-05, UC-06, UC-07, UC-08 | **Must Have** | A local prompt remains available when the external model fails; if the local service is unavailable, the system shows an error and allows retry |
| **NFR-03** | Usability and accessibility | Obj 4 | UC-05, UC-06, UC-07, UC-08 | **Should Have** | Light and dark themes are available; main controls have clear names; correct and incorrect results are not communicated by colour alone |
| **NFR-04** | Learning-record privacy and answer protection | Obj 4 | UC-05, UC-06, UC-07, UC-08 | **Must Have** | The user can confirm deletion of learning records; public question data does not directly expose answers or hidden misconceptions |
| **NFR-07** | Clear explanations without overstating results | Obj 1, 2, 4 | UC-05, UC-07, UC-08 | **Must Have** | The radar shows attempt counts; recommendations explain their reasons; insufficient evidence is clearly labelled |
| **NFR-08** | Mobile and desktop support | Obj 4 | UC-05, UC-06, UC-07, UC-08 | **Should Have** | Text is not hidden on desktop or mobile widths, and the main controls remain usable |

## 4. Current Personal Status

| Use case / requirement | Current status |
| --- | --- |
| UC-05 / FR-04 | Basic dimension statistics and the radar exist; complete exception handling still needs work |
| UC-06 / FR-07 | Attempts are stored, but the history filters and retry page are not complete |
| UC-07 / FR-06 | The recommendation feature has not been implemented |
| UC-08 / FR-05 | Local prompts and model-failure fallback exist; misconception-specific follow-up still needs work |
| FR-08, FR-09 and FR-10 | Some basic support exists; the group should verify the final version |

## 5. Personal Acceptance IDs

| Requirement ID | Acceptance IDs |
| --- | --- |
| FR-04 | AT-05-01, AT-05-02, AT-05-03, AT-05-04, AT-05-05 |
| FR-05 | AT-08-01, AT-08-02, AT-08-03, AT-08-04, AT-08-05, AT-08-06 |
| FR-06 | AT-07-01, AT-07-02, AT-07-03, AT-07-04, AT-07-05 |
| FR-07 | AT-06-01, AT-06-02, AT-06-03, AT-06-04, AT-06-05, AT-06-06 |
| FR-08 | AT-07-01, AT-07-02, AT-08-01, AT-08-06 |
| FR-09 | AT-08-03 |
| FR-10 | AT-05-03, AT-05-05, AT-06-04, AT-06-05 |
| NFR-02 | AT-08-02, AT-08-04 |
| NFR-03 | AT-05-01, AT-06-01, AT-08-01 |
| NFR-04 | AT-05-05, AT-06-04, AT-06-05 |
| NFR-07 | AT-05-02, AT-07-04, AT-08-01, AT-08-06 |
| NFR-08 | AT-05-01, AT-06-01, AT-08-05 |

## 6. Handover

The work of 50106035 can proceed in parallel with the work of 50106038.
After 50106038 completes UC-01 to UC-04, the group only needs to align shared
terms such as learning records, knowledge-point names, misconception names and
requirement IDs. This file does not include or replace 50106038's work.

## 7. Items for Group Review

1. 50106038 should merge these personal entries into the complete group RTM;
2. 50106070 should confirm the final objectives and priorities;
3. 50106034 should check the consistency of requirements and acceptance criteria;
4. The complete group RTM should still include FR-01 to FR-03 and the related NFRs.


---

## 3. Conflicting source IDs requiring a group decision (no changes made)

The entries below are **not corrections to Zhang's content**. They document collisions between the existing repository baseline and Zhang's personal RTM; rows must not be silently treated as the same requirement in a test trace.

| ID | Repository `docs/REQUIREMENTS_TRACEABILITY.md` | Zhang Zijian's original personal RTM |
| --- | --- | --- |
| FR-04 | Progressive help | Five-dimension learning radar |
| FR-05 | Item-specific evidence | Socratic guided follow-up |
| FR-06 | Question-specific subgraph | Adaptive supplementary recommendation |
| FR-07 | Guided tutoring | Search/filter/retry wrong-answer history |
| FR-08 | Attempt history and metrics | Evidence/source/review status |
| NFR-02 | Offline reliability | Model/service failure fallback |
| NFR-03 | Explainability | Usability/accessibility |
| NFR-04 | Accessibility | Privacy/answer protection |
| NFR-07 | API response performance | Clear explanations, no overstated results |
| NFR-08 | Maintainability | Desktop/mobile support |

**Scope difference:** The original task package calls UC-03 open-ended concept keyword search. The supplied application currently supports evidence review and a question-specific graph instead. Only the Lin-authored UC-03 was adjusted to the implementation; Zhang's use cases remain as written. The final supervisor/team decision must confirm how to handle the older task scope and how to resolve duplicate requirement IDs before tests are treated as a unique traceability matrix.

**Evidence caution:** There are six project-authored demonstration items labelled `Source review pending`, while Objective 2 requires at least 15 formally source-reviewed items. UC-07 adaptive recommendation is not yet implemented according to Zhang's own status note. Neither is marked as delivered or passed.

## 4. References and sign-off

- Formal project baseline: `docs/PROJECT_PROPOSAL_DRAFT.md`.
- Existing repository requirement definitions: `docs/REQUIREMENTS_TRACEABILITY.md`.
- Implementation evidence: `server.py`, `frontend/app.js`, `data/curated/questions.json`, `tests/test_server.py`, `tools/validate_project.py`.
- Colleague's frozen source: GitHub PR #5, snapshot commit `9413a58`.
- Lin's use cases: `reports/use_cases.md`, Part A.

**Review required:** Requirements lead (50106038), business analyst (50106035), group lead (50106070) and technical report reviewer (50106034) to approve a *single canonical numbering scheme* before using this combined file as a final signed-off group RTM.

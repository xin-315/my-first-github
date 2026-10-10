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
| :---: | --- | :---: | :---: | :---: | --- |
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

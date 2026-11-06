# JC2001 Group 5 — Cycle 4 Task Assignment

**Cycle:** 3–30 November 2026  
**Theme:** Evidence-led PoC development, verification, and individual technical understanding  
**Project:** StudyGraph

## 1. Purpose

Cycle 4 will advance a small, demonstrable Proof-of-Concept (PoC) slice and verify it against the agreed project objectives. The team will prioritise work that can be explained, reproduced, and tested over broad feature claims.

Every member is responsible for understanding the work they contribute. AI tools may support the work in accordance with university guidance, but members must review and take responsibility for their own work and be able to explain and demonstrate it.

The project proposal schedules GraphRAG, dynamic quiz, and verification milestones during November. The exact feature scope remains subject to the current agreed project scope and supervisor guidance. Do not present a proposed feature as completed until it has been implemented and verified.

## 2. Working Rules

1. All Cycle 4 task documents, code comments, commit messages, pull requests, test descriptions, and deliverables must be written in English.
2. Keep each change small and reviewable. Before implementation, record the problem, expected behaviour, affected files, and a testable acceptance criterion.
3. Do not claim work that has not been implemented or verified. Record limitations, failed attempts, and unresolved questions.
4. AI assistance must follow university guidance. Each member must review, understand, and take responsibility for submitted work.
5. Do not add credentials, personal data, or unverified performance claims to the repository.
6. A task is not complete until its owner can explain the change and demonstrate the relevant test or workflow.

## 3. Individual Assignments

> **Per-member task packs:** the table below is the single source of truth. A dedicated, copyable task pack for each member lives in [`reports/cycle4_task_packs/`](cycle4_task_packs/), with one file per owner and a link to that member's personal folder under `reports/final_report/`. If a pack and this document disagree, this document wins.

| Member | Responsibility | Required evidence |
|---|---|---|
| **Siqin Dong (50106060)** | Define the question-parsing and misconception-diagnosis slice; document its input, output, and failure cases. Coordinate with Yusai Xi on quiz content and the mastery-dashboard data contract. | A short design note, one working vertical slice or an evidenced blocker, tests for representative valid and invalid inputs, and a documented interface/data contract with sample cases. |
| **Hao Jiang (50106065)** | Prototype the GraphRAG retrieval path with a clearly bounded dataset and explain how retrieved graph evidence affects the response. | A runnable prototype, a baseline comparison, reproducible checks, and a note describing cases where retrieval does not help. |
| **Yuxuan Wu (50106070)** | Coordinate scope, integration, and weekly checkpoints; maintain the decision and risk log. | An English integration checklist, reviewed pull requests, and weekly status summaries containing verified evidence and open risks. |
| **Yusai Xi (50105989)** | Specify and prototype the dynamic-quiz user flow, including loading, error, and empty states. | An interactive flow or scoped prototype, acceptance checks, and a short explanation of the relevant UI decisions. |
| **Mingjie Yang (50106061)** | Own backend and integration test coverage for the Cycle 4 slice, including failure behaviour. | Tests that run from a clean checkout, recorded results, and an explanation of what each test proves and does not prove. |
| **Weixin Xie (50106034)** | Independently review requirements traceability and benchmark methodology; check that claims match evidence. | A traceability update, a reproducible evaluation procedure, and a review log identifying unsupported or ambiguous claims. |
| **Sijian Wang (50106045)** | Review architecture and data-flow changes; update diagrams only when they reflect implemented behaviour. | An architecture/data-flow note, updated diagram sources where needed, and a walkthrough linking diagram elements to actual code. |
| **Zixuan Liang (50106037)** | Maintain the runnable package and reproducibility instructions for the Cycle 4 prototype. | A clean-start run-through, dependency/configuration notes, and a documented offline or failure fallback where applicable. |
| **Yongtong Lin (50106038)** | Review user needs and acceptance criteria for the selected PoC slice; check that user-facing behaviour is understandable. | English user scenarios, acceptance criteria, and evidence from trying the implemented flow. |
| **Wenxi Luo (50106012)** | Independently verify integration, test results, and evidence consistency. | A verification checklist, reproducible test run, and a list of discrepancies or remaining risks. |

Assignments with shared responsibilities require named owners for each deliverable at the first checkpoint. Confirm individual ownership and workload with the members before treating assignments as final.

## 4. Checkpoints

- **3–7 November:** Agree the bounded feature slice, acceptance criteria, and technical approach. Each owner explains the intended change before implementation.
- **By 15 November:** Demonstrate the initial parser/retrieval prototype or document a specific blocker with evidence.
- **By 22 November:** Demonstrate the selected quiz or dashboard slice and its failure states.
- **By 25 November:** Prepare Project Update 3 evidence and report progress accurately.
- **By 30 November:** Run the verification suite, record results, review limitations, and present the integrated Cycle 4 prototype.

These are planning targets based on the repository proposal. Check them against the latest MyAberdeen schedule and supervisor instructions.

## 5. Understanding Checkpoints

At each checkpoint, the member explains in English:

- What problem the change addresses.
- How the relevant code or workflow works.
- Why the chosen approach was used and what alternative was considered.
- What the tests demonstrate and what they do not demonstrate.
- One failure, limitation, or unresolved question.

The reviewer may ask follow-up questions and request a small live walkthrough or change. The assessment criteria and status labels are visible to everyone; the exact questions are not distributed in advance.

Each member's task record must show one of these statuses:

- `UNDERSTOOD`: The member explained the work and demonstrated the relevant behaviour or test.
- `NEEDS REVIEW`: The member could not yet explain or demonstrate part of the work. Record the specific gap and agree a follow-up action.

`NEEDS REVIEW` is a learning status, not a punishment. Do not describe an item as understood until the member has reviewed it and can explain it independently.

## 6. Cycle 4 Definition of Done

Cycle 4 is complete when:

- The agreed PoC slice runs from the documented setup instructions.
- Automated tests cover changed behaviour and relevant failure cases.
- Integration and evaluation results are reproducible and accurately reported.
- Each member has an English contribution record and an understanding status for their assigned work.
- Known limitations, failed attempts, and risks are recorded rather than hidden.
- The team has a short demonstration showing the implemented behaviour and its evidence.

The goal is a credible, explainable prototype, not a claim that every proposed feature is complete. Any substantial change to the agreed project scope should be discussed with the supervisor.

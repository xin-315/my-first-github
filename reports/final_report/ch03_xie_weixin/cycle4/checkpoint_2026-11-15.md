# 15 November 2026 checkpoint — requirements and evaluation review

Assigned owner: Weixin Xie (50106034). State: IN PROGRESS.
Baseline: `5687727e903311a081896208e800e1d0f6c322cf` (remote master rechecked on 15 November 2026).

## Scope and acceptance criteria

Review the implemented parser and local diagnosis slice against recorded requirements; distinguish observed behaviour from unsupported report claims. The individual outputs are a traceability update, a reproducible evaluation procedure and an evidence-backed review log. This checkpoint does not claim completion of the team's entire Cycle 4 prototype.

Acceptance for this review: preserve source-qualified requirement IDs; link conclusions to code or raw observations; provide executable checks; record limitations and follow-up roles. The explanation checkpoint and team acceptance remain pending.

## Submitted outputs

| Output | Evidence |
| --- | --- |
| Requirements traceability | [traceability_update.md](traceability_update.md) and its CSV cover the 25 inherited FR/NFR rows and separately assess Chapter 2 R01–R14 |
| Reproducible evaluation | [evaluation_procedure.md](evaluation_procedure.md), [run_review.py](run_review.py) and pinned dependencies |
| Claims review | [review_log.md](review_log.md): 12 open findings, supporting evidence, proposed corrections and suggested follow-up roles |
| Checkpoint verification | [15 November raw evidence](evidence/2026-11-15/): regression output, JUnit XML and rerun observations |

## Verification on 15 November

The checks were rerun in a fresh virtual environment using the supplied pinned dependencies. The existing suite passed 232 tests with 17 warnings. All 68 option checks passed across 17 questions, 9 subjects and 51 traps. The valid parser pack accepted 2 questions with no issues. The invalid pack accepted none and reported 12 errors and 1 warning, exiting with status 1 as expected.

These checks support in-bank consistency and parser behaviour. They do not establish independent subject correctness, improved learning, hallucination reduction or a completed live retrieval comparison. Local timings are environment-specific and are preserved in the raw JSON rather than treated as a general performance guarantee.

The original 9 November evidence is preserved in the parent evidence directory. References to 2025 in the review prose have been corrected to 2026 to match its original timestamps. Today's evidence is stored separately.

## Open issues and next actions

The findings include answer disclosure before submission, permissive invalid-input handling, static report statistics and unsupported audit/baseline claims. Keep them open until the relevant owners resolve the agreed product or documentation contracts. Finding a defect is part of this review; this checkpoint does not claim to have repaired those defects.

Browser accessibility, responsive layout, cold-cache offline operation, independent content review and live model comparisons remain unverified. Recheck this review against later code changes before the 22, 25 and 30 November checkpoints.

Next actions are the recorded explanation checkpoint, team review and any agreed follow-up fixes. Record UNDERSTOOD after the explanation and demonstration have taken place. Record submission and merge status after the actual GitHub action.

# Results, discrepancies and limits

Verification date: 15 November 2026. Base: `5687727e903311a081896208e800e1d0f6c322cf`.

| Run | Passed | Expected failures | Other failures | Evidence |
|---|---:|---:|---:|---|
| Unchanged existing suite | 232 | 0 | 0 | `evidence/baseline.xml`, `evidence/baseline.txt` |
| Added personal cases | 26 | 4 | 0 | `evidence/personal.xml`, `evidence/personal.txt` |
| Second clean checkout, personal | 26 | 4 | 0 | `evidence/clean/personal.xml`, `evidence/clean/personal.txt` |
| Second clean checkout, all tests | 258 | 4 | 0 | `evidence/clean/full.xml`, `evidence/clean/full.txt` |

The baseline includes the 49 existing parser cases; these are not new personal contributions. The full suite is 232 existing passes + 26 new passes + 4 new expected failures, 262 collected cases. The XML records four skipped elements of type `pytest.xfail`; this is pytest's JUnit representation of expected failures. Do not add them to the pass total. Each run emitted 17 existing dependency deprecation warnings. No performance target was measured.

The second checkout was cloned locally from the unchanged base and received only the submission's new test and personal folder. `evidence/clean/environment.json` records Python, platform, installed package versions, commands, timestamps and exit codes. `tracked_changes` was empty there: tracked production files were unchanged; submitted additions were untracked overlays. The same newly installed isolated venv was reused, so this proves clean source reproduction with that environment, not an independent second OS or a second dependency installation.

## C4-01: invalid UTF-8 is treated as an unexpected validator failure

Input: a negative byte fixture `FF FE`, not new question content. `parse_question_pack_file` catches JSONDecodeError and OSError but not UnicodeDecodeError. The file API raises; the CLI catches it in its unexpected-error handler and exits 2. The CLI module documents read/decode errors as exit 1, and the file API promises reported issues instead of raised file errors.

Two strict expected-failure tests retain the intended API/exit expectations. Suggested follow-up for the parser owner: handle UnicodeError as a structured input issue, verify CLI exit 1, then remove the xfail markers after review. No fix is claimed in this test-only submission.

## C4-02: export is not lossless for optional content

Input: existing seed questions with a graph or Socratic prompt. Export writes the core fields, options and traps but omits graph and socratic_prompt. Re-parsing succeeds but those fields are None; the two preservation expectations fail. This can change `knowledge_nodes` and offline guidance in diagnosis. The earlier core round-trip test does not compare these fields.

Two strict expected-failure cases record this boundary. The tests' preservation expectation is stronger than the current exporter; the product owner should decide whether export must be lossless or be explicitly documented as a reduced format. Until then, do not claim full round-trip preservation. No graph retrieval functionality is implied by the existence of seed graph labels.

## Coverage limits

- The two sample questions and existing seed bank are provenance fixtures, not evidence of educational correctness or improved learning. Percentages and factual claims embedded in their text were not independently evaluated.
- Wrong-type HTTP inputs are rejected with 422; semantic unknown IDs instead produce the existing 200 fallback. Repository exceptions produce a distinct failsafe. Returning 200 is not proof of a useful diagnosis: inspect fallback/model/trap fields.
- The HTTP integration tests inject a parsed repository into the real router. They prove routing, request normalization, service integration and response serialization under this fixture, not a production import pipeline or browser workflow.
- MockTransport simulates timeout, HTTP 503, invalid JSON and empty output. It verifies fallback selection and retained trap fields, not real provider availability, wall-clock timeout compliance, model quality, privacy or live authentication.
- Mixed invalid packs can retain valid models in the parser result. The CLI checks global usability before side effects; other callers must make their own gate decision.
- No new GraphRAG retrieval, dashboard, load/security test, real-user trial, or team-wide acceptance is claimed. Unexamined CLI option combinations and export filesystem failures remain outside these cases.
- The host setup had temporary-directory and local Git subprocess permission failures; the permission-assisted setup succeeded. Reproducibility on other hosts still requires checking the documented environment.

Repeated deprecation-warning source excerpts were removed from the initial text transcripts to avoid copying unrelated auth-model examples; test outcomes and warning counts are retained, with the omission marked. The clean-run commands suppress those excerpts directly. No live credentials, real user-trial records or new participant data were added.

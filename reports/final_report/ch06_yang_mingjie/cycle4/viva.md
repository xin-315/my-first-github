# Walkthrough notes

Practice notes for the English discussion. The teacher's actual questions are not known.

## Short introduction

My part is testing the backend workflow from a question pack to a diagnosis. The parser was already merged, so the tests use the existing sample packs and seed questions. They check the selected answer, the matching trap, HTTP fields and failure behaviour. The new tests have 26 passes and four expected failures. Those failures show two remaining problems: invalid UTF-8 handling and information lost during export. The full run has 258 passes, including the team's 232 existing tests.

## Code walkthrough

1. Open `backend/app/services/question_parser.py`: `parse_question_pack_file` reads UTF-8 JSON and calls `parse_question_pack`. Inspect `ParseResult.ok`, `questions` and `issues`; a partial list is not unconditional acceptance.
2. Open `scripts/validate_question_pack.py`: `usable` gates export and diagnosis. `--strict` also rejects warnings.
3. Open `backend/app/services/quiz_service.py`: each explicitly provided question list becomes the lookup repository.
4. Open `backend/app/services/diagnostic_service.py`: the constructor accepts `quiz_repo`; the selected option finds a trap, and that trap supplies prerequisite/radar information. Correct answers use rules. Wrong answers use provider guidance when available or local fallback.
5. Open `tests/test_cycle4_integration.py`: explain one parametrized case, one MockTransport branch, and one CLI side-effect assertion. Open the matching matrix row and recorded XML.

## Practice questions and answer points

**What is your contribution?** The additional integration tests, run script, recorded results and test matrix. The parser and diagnosis implementation were already in the repository. Personal review and demonstration are still pending.

**Why is checking HTTP 200 insufficient?** A fallback also returns 200. I check trap identifiers, correct answer, score, model identifier and fallback mode so an unrelated emergency response cannot be mistaken for a correct diagnosis.

**Give a concrete case.** In the shipped sample, `cs_2` option B maps to `trap_cs_2_1`, radar `precision`, score -5. With no API key it uses `local-knowledge-seed`. Option A is correct and uses rule evaluation with score +5. These are fixture mappings, not measured learning outcomes.

**Why MockTransport rather than a real API?** It makes HTTP 503, invalid JSON, empty output and a raised timeout deterministic without credentials. It still executes the service's HTTP response handling. It does not measure a real four-second deadline or prove provider reliability. A live test would be a separate evaluation.

**Why record a call count?** The service catches exceptions. An assertion raised inside a mocked provider function could be swallowed by fallback and let a weak test pass. Recording the calls lets the test assert outside that catch block that no call happened when the answer is correct or Socratic generation is disabled.

**What is the difference between an unknown question and a broken repository?** An unknown ID returns `trap_fallback`, model `local-safe-fallback`, score -2. A repository exception returns `trap_failsafe`, model `local-failsafe-shield`, score 0. Neither is a successful real question evaluation.

**What does the HTTP test inject?** Only the router module's diagnostic-service object, scoped by pytest's monkeypatch. The real route, request model, service and response model run. This is not evidence of a production pack-upload endpoint.

**Why use a subprocess for the CLI?** Calling `main()` alone cannot prove the entry-point import path, process exit code or independence from the current working directory. The subprocess uses the test interpreter and an external temporary working directory.

**Why test mixed packs?** A parser result may retain valid questions even when another question has errors. The CLI must inspect the whole result before exporting or diagnosing. I use an existing valid question with an explicitly mutated empty stem and verify that an existing output sentinel is not overwritten.

**Are four xfails four passes?** No. They are four intentionally failing expectations for two unresolved issues. Strict xfail makes an unexpected future pass fail the suite for review. A zero test-process exit code must be read alongside the count and issue record.

**What exactly is lost on export?** The tested existing seed graph and Socratic prompt are omitted. Re-parsing still succeeds, so a core-only round-trip test misses it. The owner must decide between preserving these fields and explicitly defining export as reduced; I have not silently fixed another member's feature.

**What remains to be done?** The two reported issues need review, and the suite needs to be rerun when later changes are integrated. My English explanation and demonstration are still pending. This run does not cover the dashboard, retrieval or a user trial.

## Live demonstration and small change

Run the three README demonstration commands. Explain exit 0 for the valid local diagnosis and exit 1 for the invalid pack. Run `python -m pytest tests/test_cycle4_integration.py -q -rx --disable-warnings` and show both pass and xfail counts.

For a small walkthrough, select only `test_sample_option_mapping` with `-k sample_option_mapping`: eight sample selections should pass. Explain why changing the expected `cs_2:B` radar from precision to boundary would fail. If asked to make that change live, make it on a temporary branch/copy, show the failed assertion, then restore the original expectation and rerun. Do not alter submitted evidence to conceal the deliberate failure.

Finish by opening `results.md` and explaining one unresolved issue and one coverage limit in your own words.

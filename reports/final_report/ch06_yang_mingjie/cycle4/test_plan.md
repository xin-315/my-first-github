# Cycle 4 personal verification plan

Owner: Mingjie Yang (50106061). Recorded before adding the tests, 15 November 2026.
Base: master `5687727e903311a081896208e800e1d0f6c322cf`.

## Why these tests are needed

The merged parser already has unit tests, but the CLI tests call main() in the same process. The new tests will check how the existing sample reaches the diagnosis service and HTTP response, whether the CLI works from another directory, and how failures are handled. The scope is the current backend workflow.

## Expected behaviour and acceptance criteria

1. Every A-D selection in the existing two-question valid sample must retain the expected correct answer, trap, radar dimension and explanation through diagnosis.
2. The real HTTP route must preserve aliases and reject invalid field types when a parsed repository is injected for testing only.
3. Separate parsed repositories must not contaminate one another or the default seed repository.
4. Simulated upstream failures and a repository exception must produce the implemented fallback response, without a real external request.
5. A separate CLI process must run outside the repository working directory, accept the shipped valid pack, reject the shipped invalid pack, and refuse export/diagnosis of a mixed invalid pack. Strict warnings must block export.
6. Probe documented file error and round-trip expectations. If unmet, retain strict expected-failure regressions with an issue explanation; do not report them as passing functionality.

Affected files: new `tests/test_cycle4_integration.py`, personal `cycle4/` documentation and evidence, and the personal task-pack status only. Production code and existing tests are not changed.

## Method and alternatives

Use the shipped `ch05_dong_siqin/cycle4/samples/valid_pack.json`, invalid sample, and `SEED_QUESTIONS`. Negative inputs are explicitly labelled mutations, not newly claimed product content. TestClient exercises ASGI without starting a server. A subprocess checks the real CLI entry point. MockTransport simulates upstream responses deterministically. A live API test was rejected for this verification because it requires credentials and is nondeterministic; no claims about live model quality or network timing follow.

Run the unchanged suite first, followed by the new tests and full suite. Repeat from a second clean Git checkout with the submission files added. Keep the dependency versions, results and a per-test explanation. The November 3-7 planning meeting has not been verified in this record.

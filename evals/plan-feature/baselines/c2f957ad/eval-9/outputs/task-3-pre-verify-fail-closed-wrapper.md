# Task 3 — Make the pre-verify wrapper fail closed on any non-zero gate exit

**Summary**: TC-9008: Make pre-verify.sh fail closed on gate errors instead of grepping stderr for 401/403
**Issue type**: Task | **Labels**: ai-generated-jira | **Priority**: Major (inherited) | **fixVersions**: omitted (Feature has none)
**Links**: TC-9008 incorporates this task; depends on Task 2

---

## Repository
release-verifier

## Target Branch
main

## Description
`scripts/pre-verify.sh` runs the gate before verification. It reports authentication failures only by grepping client stderr for 401/403, and the Feature's Known Risks note that an empty `[]` never triggers this. With the gateway's successful-empty response to unauthenticated requests, the wrapper lets the run continue as a normal skip and finishes green.

This task makes the wrapper **fail closed**. Any non-zero exit from the gate or client stops the run with a non-zero exit and an error message. Only an explicit, successful skip outcome from the gate (Task 2) skips verification. Only a successful verify outcome runs the suite.

## Files to Modify
- `scripts/pre-verify.sh` — decide on the gate's exit status and explicit outcome, not on a 401/403 grep of stderr. Propagate non-zero exits and fail the run

## Files to Create
- `tests/scripts/test_pre_verify.py` — tests that run `scripts/pre-verify.sh` against a stubbed gate to cover the verify, skip and error outcomes

## Implementation Notes
- **Gate and skip site**: `scripts/pre-verify.sh` currently greps client stderr for 401/403 to report auth failures, and otherwise treats the gate's result as success or skip. Put the fail-closed guard where the wrapper reads the gate's result:
  - Enable `set -euo pipefail` (or check `$?` explicitly) for the gate invocation.
  - Treat **any** non-zero gate exit as a hard failure that exits non-zero.
  - Keep the 401/403 grep, if at all, only to improve the error message. It must not be the condition that decides failure.
- Read the skip outcome only from the explicit skip signal that Task 2 defines (for example a distinct exit code or stdout marker from `resolve_gated_issue`). Never infer a skip from empty output.
- Make sure the gate is not run in a pipeline or subshell that hides its exit status (for example `gate | tee` without `pipefail`).
- A post-merge live run with the real token is a supplementary operational check only. It does not replace the tests below.
- Test placement: no shell test location exists yet. The new test sits in a new `tests/scripts/` directory next to the existing `tests/tracker/` and `tests/gate/` pytest suites, and calls the script with `subprocess`. Stub the gate entry point through `PATH` or an env override.
- Constraints (docs/constraints.md):
  - §1.4/§5.1: limit changes to the listed files.
  - §5.2: inspect `pre-verify.sh` first.
  - §5.8: error-handling parity with the Python gate.
  - §5.11–5.13: test doc and given-when-then comments.
  - §2.1–2.3: commit rules.
  - §3.1–3.3: PR rules.

## Reuse Candidates
- `scripts/pre-verify.sh` (existing gate invocation and error reporting) — extend it in place
- `tests/gate/test_resolve_issue.py` — follow its pytest conventions for the new wrapper test

## Acceptance Criteria
- [ ] **Fail-closed**: when the gate or tracker client exits non-zero for any reason (including `TrackerAuthError` from an unauthenticated empty search), `scripts/pre-verify.sh` exits non-zero and prints an error. It does not skip and does not exit 0.
- [ ] Deciding on auth failure no longer depends on 401/403 appearing in stderr. A non-zero exit with no 401/403 text still fails the run.
- [ ] When the gate exits successfully with an explicit skip outcome, the wrapper skips verification, logs the skip and exits 0.
- [ ] When the gate exits successfully with a verify outcome, the wrapper continues to the verification suite.

## Test Requirements
- [ ] **Fail-closed test**: stub the gate to exit non-zero with no 401/403 text in stderr, simulating the unauthenticated empty-search path rejected by Task 2. Assert `pre-verify.sh` exits non-zero and does not report a skip.
- [ ] A test stubs the gate to exit non-zero with 401 in stderr and asserts the wrapper exits non-zero.
- [ ] A test stubs the gate to return the explicit skip outcome and asserts the wrapper exits 0 and logs the skip.
- [ ] A test stubs the gate to return the verify outcome and asserts the wrapper proceeds to verification.

## Verification Commands
- `pytest tests/scripts/test_pre_verify.py` — all tests pass
- `bash -n scripts/pre-verify.sh` — no syntax errors

## Dependencies
- Depends on: Task 2 — Gate verification on a "Ready for Verification" linked issue; fail closed on unproven-auth empty search

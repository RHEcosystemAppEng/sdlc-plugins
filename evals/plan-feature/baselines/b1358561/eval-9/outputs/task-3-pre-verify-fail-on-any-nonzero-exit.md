**Summary:** Make pre-verify.sh fail on any non-zero gate exit instead of grepping for 401/403
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9008)
**Parent:** Epic "TC-9008: Fail-closed tracker-gated release verification"

## Repository
release-verifier

## Target Branch
main

## Description
`scripts/pre-verify.sh` runs the gate before verification. It reports an authentication failure only by grepping the client's stderr for 401/403, and only when the client exits non-zero. The Feature's Known Risks note that an empty `[]` never triggers this, and that other failure messages (e.g. the new `TrackerAuthError` from Task 1 for unproven authentication) would not match the grep either. This task makes the wrapper fail closed. Any non-zero exit from the gate fails the pre-verify step. Skipping verification requires an explicit skip outcome from the gate, never just the absence of an error.

## Files to Modify
- `scripts/pre-verify.sh` — run with `set -euo pipefail` (or check the gate's exit code explicitly). Fail the step on any non-zero gate exit and surface stderr. Proceed to verification only on an explicit "verify" outcome, and skip only on an explicit "skip" outcome

## Files to Create
- `tests/scripts/test_pre_verify.py` — pytest tests that run `scripts/pre-verify.sh` via `subprocess` with a stubbed gate command, covering verify, skip, and failure exits

## Implementation Notes
- **Fail-closed gate site:** `scripts/pre-verify.sh`, at the step that runs the gate and the stderr grep for 401/403. Replace the grep-based detection with exit-code handling. Keep the 401/403 message as diagnostic output only if useful; it must not be the condition that decides failure.
- Define an explicit exit-code contract with the gate from Task 2 (`src/gate/resolve_issue.py::resolve_gated_issue`): for example `0` = verify, a dedicated code such as `78` = skip (logged), and any other non-zero = error, which fails the run. Alternatively, have the gate print an explicit `VERIFY`/`SKIP` decision on stdout and treat anything else as an error. Pick one and document it at the top of the script.
- Make the gate command overridable (e.g. an environment variable defaulting to the real gate invocation) so the new tests can substitute a stub that exits with a chosen code. This avoids network calls in tests.
- An operational post-merge live run may confirm the token works, but it is not the coverage for this risk. The subprocess tests below are.
- Constraints (docs/constraints.md): §2.1–2.3 commit rules. §3.2–3.3 PR rules (`--base main`). §5.1–5.4 and §5.11–5.12 code-change and test-documentation rules. §1.4–1.5 implement-task scope.

## Reuse Candidates
- `scripts/pre-verify.sh` — existing gate invocation and logging. Restructure its control flow rather than adding a second wrapper
- `tests/gate/test_resolve_issue.py` — existing pytest layout and fixtures for gate tests. Follow its style for the new script tests

## Acceptance Criteria
- [ ] When the gate exits with the "verify" outcome, the wrapper continues to the verification suite
- [ ] When the gate exits with the explicit "skip" outcome, the wrapper skips verification, logs the reason, and exits 0
- [ ] **Fail-closed:** when the gate exits with any other non-zero code, including a `TrackerAuthError` failure whose stderr contains no "401" or "403", the wrapper exits non-zero and does not skip or report success
- [ ] Failure detection no longer depends on stderr containing 401/403

## Test Requirements
- [ ] Test that a stub gate returning the verify outcome makes the wrapper proceed (e.g. it invokes a stubbed verification command)
- [ ] Test that a stub gate returning the explicit skip outcome makes the wrapper exit 0 without running verification
- [ ] **Degraded-path test:** a stub gate that exits non-zero with stderr `TrackerAuthError: authentication could not be proven` (no 401/403 text) makes the wrapper exit non-zero, and verification is neither run nor reported as passed
- [ ] Test that a stub gate exiting non-zero with 401 in stderr still makes the wrapper exit non-zero (regression)

## Dependencies
- Depends on: Task 2 — Gate verification on a "Ready for Verification" linked issue with fail-closed resolution

# Task 3 — Make the pre-verify wrapper fail closed on gate errors instead of grepping for 401/403

**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9008)
**Fix Versions:** (omitted — TC-9008 has none)

## Repository
release-verifier

## Target Branch
main

## Description
`scripts/pre-verify.sh` runs the gate before the verification suite and reports an authentication failure only by grepping the client's stderr for 401/403. TC-9008's Known Risks note that this wrapper only reports auth failures when the client exits non-zero, which an empty `[]` from the gateway never triggers — so the run proceeds as a green skip.

This task makes the wrapper honor the gate's exit status from Task 2: any non-zero gate exit (including the unverified-authentication error) fails the pre-verify step, and only an explicit skip marker from a successful gate run results in a skip. The suggested "live run after merge" mitigation is kept only as a supplementary check, not as the coverage for this risk.

## Files to Modify
- `scripts/pre-verify.sh` — propagate the gate's exit code, fail on non-zero, and require an explicit verify/skip result before continuing

## Files to Create
- `tests/scripts/test_pre_verify.py` — tests that invoke `scripts/pre-verify.sh` with a stubbed gate and assert its exit status for verify, skip, and unverified-auth paths

## Implementation Notes
- **Skip/gate site:** `scripts/pre-verify.sh`, the block that runs the gate and greps stderr for `401`/`403`. Replace the grep-based detection with exit-status handling:
  - Enable `set -euo pipefail` (or capture `$?` explicitly) so the gate's exit status is not lost through pipes such as `... 2>&1 | grep`.
  - If the gate exits non-zero for any reason (including Task 1/2's `TRACKER_AUTH_UNVERIFIED` error), print an error and `exit` non-zero — do not fall through to "skip".
  - Treat the run as a skip only when the gate exited 0 **and** emitted the explicit skip marker defined in Task 2; treat it as verify only when the gate exited 0 and emitted an issue key. Any other combination (exit 0 with empty/unexpected output) is a failure.
  - The stderr grep for 401/403 may remain as an extra diagnostic message, but must not be the condition that decides failure.
- Tests: drive the script with a stub gate executable on `PATH` (or an env override for the gate command) that returns the desired exit code/output; assert the script's exit code.
- Post-merge: a live verifier run against the gateway with the service-account token may be performed as a supplementary smoke check. It does not replace the fail-closed acceptance criteria and tests in this task and in Tasks 1–2.
- Constraints (docs/constraints.md): Conventional Commits with Jira footer and `Assisted-by:` trailer (§2.1–2.3); branch named after task ID, `--base main`, PR link on Jira (§3.1–3.3); scope limited to listed files, inspect before modifying (§5.1–5.4); test doc comments and given-when-then for non-trivial tests (§5.11–5.12).

## Reuse Candidates
- `scripts/pre-verify.sh` — existing gate invocation and error-reporting block; modify in place rather than adding a new wrapper
- `src/gate/resolve_issue.py::resolve_gated_issue` — exit-code / skip-marker contract defined in Task 2

## Acceptance Criteria
- [ ] **Fail-closed:** when the gate exits non-zero because the tracker source cannot be proven authenticated (empty search from the gateway with unverified auth), `scripts/pre-verify.sh` exits non-zero and the verification run does not finish green.
- [ ] **Fail-closed:** when the gate exits 0 but emits neither an issue key nor the explicit skip marker (empty/unexpected output), `scripts/pre-verify.sh` exits non-zero.
- [ ] When the gate exits 0 with the skip marker, the script skips verification with a log message and exits 0.
- [ ] When the gate exits 0 with a "Ready for Verification" issue key, the script proceeds to verification.
- [ ] Failure detection no longer depends on grepping stderr for 401/403.

## Test Requirements
- [ ] **Fail-closed test:** stub the gate to exit non-zero with `TRACKER_AUTH_UNVERIFIED` and no 401/403 text on stderr; assert `scripts/pre-verify.sh` exits non-zero and does not report a skip.
- [ ] **Fail-closed test:** stub the gate to exit 0 with empty stdout; assert the script exits non-zero.
- [ ] Test: gate exits 0 with the skip marker → script exits 0 and logs the skip.
- [ ] Test: gate exits 0 with an issue key → script proceeds to verification (verification command stubbed).

## Verification Commands
- `pytest tests/scripts/test_pre_verify.py` — all tests pass
- `bash -n scripts/pre-verify.sh` — no syntax errors

## Dependencies
- Depends on: Task 2 — Gate verification on a "Ready for Verification" linked issue and fail closed on unauthenticated empty results

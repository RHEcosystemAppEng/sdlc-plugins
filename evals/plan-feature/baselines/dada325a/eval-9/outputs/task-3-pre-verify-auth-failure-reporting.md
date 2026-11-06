# Task 3 — Make pre-verify.sh fail closed and report auth failures from the gate exit status

**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9008)
**Fix Versions:** (omitted — Feature has none)
**Parent Epic:** TC-9008: Fail-closed verification gate

## Repository
release-verifier

## Target Branch
main

## Description
`scripts/pre-verify.sh` runs the gate before verification and reports authentication failures only by grepping the client's stderr for 401/403. The Feature's Known Risks note that the wrapper only reports an auth failure when the client exits non-zero, which an empty `[]` never triggers. After Task 2, the gate exits with a dedicated non-zero status when tracker authentication is not proven. This task makes the wrapper act on the gate's exit status: report an authentication failure for the "auth not proven" status, fail the run for any non-zero status, and only treat the run as a skip when the gate explicitly returned a legitimate skip.

## Files to Modify
- `scripts/pre-verify.sh` — propagate the gate's exit status; map the dedicated "auth not proven" exit status (and existing 401/403 output) to an authentication-failure report; never convert a non-zero gate result into a skip/green outcome

## Implementation Notes
- Current behavior in `scripts/pre-verify.sh`: greps client stderr for 401/403 to report auth failures. Keep the 401/403 reporting, but make the exit status of the gate (`src/gate/resolve_issue.py::resolve_gated_issue`, see Task 2) the primary signal.
- Run the script with `set -euo pipefail` semantics (or explicitly capture `$?`) so a non-zero gate status cannot be masked by a pipeline into `grep`.
- Three outcomes only: verify (gate returned an issue), skip (gate returned a legitimate skip with exit 0), fail (any non-zero status; report "tracker authentication not proven" for the dedicated auth exit status). There is no path where a non-zero or unproven-auth result ends as a green skip.
- If release-verifier has no existing shell-script test harness, add the wrapper test alongside the gate tests in `tests/gate/test_resolve_issue.py` by invoking `scripts/pre-verify.sh` via `subprocess` with a stubbed gate; confirm the existing test layout at implementation time.
- Constraints (docs/constraints.md): §2 commit rules — Conventional Commits, `Implements <task-key>` footer, `Assisted-by:` trailer; §3 PR rules — branch named after the task issue ID, `gh pr create --base main`, post PR link to the Jira task; §5 code change rules — scope changes to the listed files (§5.1), inspect the script before modifying (§5.2), doc comments on every new test (§5.11).

## Reuse Candidates
- `scripts/pre-verify.sh` existing 401/403 stderr detection — keep and extend rather than rewrite

## Acceptance Criteria
- [ ] When the gate exits with the "auth not proven" status (e.g. unauthenticated gateway search returned `[]`), `pre-verify.sh` exits non-zero and reports a tracker authentication failure
- [ ] Any non-zero gate exit status makes `pre-verify.sh` exit non-zero; it is never reported as a skip or success
- [ ] HTTP 401/403 from the client are still reported as authentication failures
- [ ] A legitimate skip (gate exit 0, no linked issue with proven auth, or issue not "Ready for Verification") is still reported as a skip and verification does not run
- [ ] A "Ready for Verification" result proceeds to verification

## Test Requirements
- [ ] Fail-closed test: stub the gate to exit with the "auth not proven" status and no 401/403 text in stderr → assert `pre-verify.sh` exits non-zero and prints the authentication-failure message
- [ ] Test: stub the gate to emit 401/403 → assert authentication failure is reported
- [ ] Test: stub the gate to return a legitimate skip (exit 0) → assert the script reports a skip and exits 0
- [ ] Test: stub the gate to return a "Ready for Verification" issue → assert the script proceeds to verification

## Verification Commands
- `bash -n scripts/pre-verify.sh` — no syntax errors
- `pytest tests/gate/test_resolve_issue.py` — all tests pass, including the wrapper tests

## Dependencies
- Depends on: Task 2 — Gate verification on "Ready for Verification" and fail closed on unauthenticated empty searches

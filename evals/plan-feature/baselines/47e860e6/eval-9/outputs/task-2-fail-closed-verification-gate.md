**Summary:** TC-9008: Gate verification on a "Ready for Verification" linked issue, failing closed on unproven tracker results
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9008)
**Epic:** TC-9008: Fail-closed tracker gating

## Repository
release-verifier

## Target Branch
main

## Description
Before running the expensive verification suite, the release verifier must look up the tracker issue linked to the pull request. It verifies only when that issue is in the "Ready for Verification" state, and skips with a log message otherwise (TC-9008 MVP requirements 1 and 2).

The feature's Known Risks describe a fail-open path. An unauthenticated or under-privileged request gets a successful empty search. `resolve_gated_issue` treats the empty result as "no matching issue" and returns `None` (skip). `scripts/pre-verify.sh` reports auth failures only when the client exits non-zero, which an empty `[]` never triggers. The result is a green verifier run that never verified the PR.

This task makes the gate and its shell wrapper fail closed. A skip is allowed only when the tracker result is proven authenticated (using the guarantee from Task 1). Any unproven, degraded, or errored tracker lookup must fail the run (non-zero exit) instead of skipping.

## Files to Modify
- `src/gate/resolve_issue.py`: in `resolve_gated_issue(pr_url)`, search for the PR's linked issue. Return it for verification only when it is "Ready for Verification". Skip with a log message for other states and for a proven-authenticated empty result. Propagate/raise on `TrackerAuthUnprovenError` or any tracker error instead of returning `None`.
- `scripts/pre-verify.sh`: fail the run on any non-zero exit from the gate/client, including the dedicated auth-unproven exit code. Do not use stderr grepping for 401/403 as the only failure signal. Distinguish an explicit "skip" outcome from failure.
- `tests/gate/test_resolve_issue.py`: add tests for the ready / not-ready / no-linked-issue / degraded-empty paths.

## Implementation Notes
- **Gate/skip site (primary):** `src/gate/resolve_issue.py::resolve_gated_issue`. This is the line that returns `None` (skip) when `search_issues` returns an empty result. Add the guard here:
  - Catch nothing broader than needed. Let `TrackerAuthUnprovenError` (from Task 1) and other tracker errors propagate, or convert them into a gate error that exits non-zero.
  - Only an empty result returned **successfully** by `search_issues` (which after Task 1 means authentication was proven) may become a skip.
  - Log the skip reason explicitly: "no linked issue" vs "linked issue <KEY> in state <STATE>, not Ready for Verification".
- **Gate/skip site (wrapper):** `scripts/pre-verify.sh`. Today it greps client stderr for 401/403 to report auth failures. Change it so that:
  - `set -euo pipefail` (or explicit exit-code checks) makes any non-zero gate exit fail the job.
  - The dedicated auth-unproven exit code from Task 1 gets a clear "tracker authentication could not be proven, failing closed" message.
  - A skip is signalled through an explicit, positive outcome from the gate (for example a dedicated exit code or a structured `SKIP` output line). It must not be inferred from the absence of an error.
- Linked-issue lookup: build the JQL from the PR URL using the existing `search_issues(jql)` client. Do not add a new search client (MVP requirement 1: "Uses the existing search client").
- Status comparison: compare against the exact status name "Ready for Verification". Keep the name in a single constant so it is easy to change.
- Constraints (docs/constraints.md):
  - §2: Conventional Commits, Jira ID footer, and the `Assisted-by: Claude Code` trailer.
  - §3: branch named after the task Jira ID, `--base main`, and the PR link posted to Jira.
  - §5: change only the listed files, inspect before modifying, and reuse `search_issues`.

## Reuse Candidates
- `src/tracker/client.py::search_issues`: existing search client. Reuse it for the linked-issue lookup.
- `src/tracker/client.py::TrackerAuthUnprovenError` (added in Task 1): the fail-closed signal the gate must propagate.

## Acceptance Criteria
- [ ] A pull request linked to an issue in "Ready for Verification" is returned by `resolve_gated_issue` and proceeds to verification.
- [ ] A pull request linked to an issue in any other state is skipped, with a log message naming the issue key and state.
- [ ] A pull request with no linked issue is skipped with a log message, **only** when the tracker search succeeded with proven authentication.
- [ ] **Fail-closed:** when the tracker search returns an empty result from a source that cannot be proven authenticated or healthy (`TrackerAuthUnprovenError`, or any tracker error), `resolve_gated_issue` does not return `None` (skip). It raises, and the gate exits non-zero.
- [ ] **Fail-closed:** `scripts/pre-verify.sh` exits non-zero and reports a tracker-authentication failure when the gate/client exits with the auth-unproven code. A degraded empty search can no longer produce a green run without verification.
- [ ] `scripts/pre-verify.sh` does not depend only on grepping stderr for 401/403 to detect auth failures.

## Test Requirements
- [ ] Test: linked issue in "Ready for Verification" → `resolve_gated_issue` returns the issue.
- [ ] Test: linked issue in another state (for example "In Progress") → skip (`None`) with the expected log message.
- [ ] Test: proven-authenticated empty search → skip (`None`) with a "no linked issue" log message.
- [ ] Test (degraded/empty path): mock `search_issues` to raise `TrackerAuthUnprovenError`, simulating the gateway's successful empty response to an unauthenticated/under-privileged request. Assert `resolve_gated_issue` raises / the gate exits non-zero and does **not** return `None`.
- [ ] Test (wrapper): run `scripts/pre-verify.sh` with a stubbed gate/client that prints `[]` and exits with the auth-unproven code. Assert the script exits non-zero and prints the tracker-auth failure message (for example a bats test or a pytest `subprocess` test).
- [ ] Test (wrapper): stubbed gate signals an explicit skip → script exits 0 and does not run verification. Stubbed gate signals ready → verification runs.

## Verification Commands
- `pytest tests/gate/test_resolve_issue.py`: all tests pass, including the fail-closed case.

## Dependencies
- Depends on: Task 1 — Make tracker search fail closed when authentication cannot be proven

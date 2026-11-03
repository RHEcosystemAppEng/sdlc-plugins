# Task 2 — Gate verification on a "Ready for Verification" linked issue, and fail closed when tracker auth is unverified

**Summary:** TC-9008: Gate verification on linked "Ready for Verification" issue with fail-closed auth check in resolve_gated_issue
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9008)
**Fix Versions:** (omitted, because TC-9008 has none)
**Epic group (by-sub-feature):** TC-9008: Verification gate

## Repository
release-verifier

## Target Branch
main

## Description
Before the expensive verification suite runs, the gate must search the tracker for the issue linked to the pull request and verify only when that issue is in the "Ready for Verification" state. PRs with no matching issue, or with a linked issue in any other state, are skipped with a log message.

This task owns the gate's skip decision, which is where the fail-open risk in TC-9008 is realized. Today `resolve_gated_issue(pr_url)` returns `None` (skip) whenever `search_issues` returns `[]`. Because the gateway returns `[]` with exit 0 to unauthenticated or under-privileged requests, a verifier run can finish green without verifying the PR. The gate must fail closed. An empty result may mean "no linked issue -> skip" only after the tracker session has been positively verified as authenticated (using the check from Task 1). Otherwise the gate exits non-zero.

## Files to Modify
- `src/gate/resolve_issue.py`: search for the PR's linked issue, filter on the "Ready for Verification" status, log skip reasons, and add a fail-closed auth guard before the empty-result skip.
- `tests/gate/test_resolve_issue.py`: add tests for the verify, skip and fail-closed paths.

## Implementation Notes
- **Guard site:** `src/gate/resolve_issue.py::resolve_gated_issue(pr_url)`, at the branch that returns `None` when the `search_issues` result is empty. Before that branch, call the client's positive auth check added in Task 1 (for example `verify_authenticated()` in `src/tracker/client.py`). If the check raises, or can't confirm authentication, let the gate exit non-zero with the stable message (for example `tracker auth unverified`). Do **not** return `None`. Don't catch the auth error and turn it into a skip.
- The JQL passed to `search_issues` should find the issue linked to `pr_url` (through the PR link field the tracker stores). Reuse `src/tracker/client.py::search_issues`. Don't write a new search path.
- Result handling after auth is verified:
  - Empty result: return `None` (skip) and log "no linked tracker issue for <pr_url>; skipping verification".
  - Linked issue whose status is not "Ready for Verification": return `None` (skip) and log the issue key and its current status.
  - Linked issue in "Ready for Verification": return the issue so verification runs.
- Order of operations matters. The auth check must run (or be confirmed) before an empty result is interpreted. An auth check that runs only after a non-empty result doesn't close the risk.
- The "live run after merge" mitigation in the feature is an extra operational check only. This code-level guard and its tests are the main coverage.
- Per docs/constraints.md §2: commits must follow Conventional Commits, reference TC-9008 in the footer, and include `--trailer="Assisted-by: Claude Code"`.
- Per docs/constraints.md §3: branch named after the Jira task key. `gh pr create --base main`. Post the PR link on the Jira task.
- Per docs/constraints.md §5: limit changes to the files listed above, inspect the code before editing, and reuse the client functions rather than duplicating HTTP or auth logic.

## Reuse Candidates
- `src/tracker/client.py::search_issues`: the existing search client the feature requires.
- `src/tracker/client.py` positive auth check (added in Task 1): the source of truth for "authenticated and permitted".

## Acceptance Criteria
- [ ] PRs linked to a "Ready for Verification" issue are verified: `resolve_gated_issue` returns the issue.
- [ ] PRs with no linked issue are skipped with a log message, but only after the tracker session is verified as authenticated.
- [ ] PRs linked to an issue in any other state are skipped with a log message that names the issue key and status.
- [ ] **Fail-closed:** the gate exits non-zero when the tracker source can't be proven authenticated, instead of treating an empty search result as a skip. An unauthenticated or under-privileged gateway response (200 + `[]`) never produces a skip or a green run.
- [ ] The auth error is not caught and turned into `None` anywhere in `resolve_gated_issue`.

## Test Requirements
- [ ] Test that a linked issue in "Ready for Verification" returns the issue (verify path).
- [ ] Test that an authenticated empty search result returns `None` and logs the skip message.
- [ ] Test that a linked issue in a different status (for example "In Progress") returns `None` and logs its key and status.
- [ ] **Degraded-path test:** mock the auth check to fail (or return unauthenticated) while `search_issues` returns `[]` with exit 0. Assert that `resolve_gated_issue` exits non-zero (or raises the auth error) and does **not** return `None`.
- [ ] Test that the auth check runs before an empty result is treated as a skip (for example, assert the call order on the mock).

## Verification Commands
- `pytest tests/gate/test_resolve_issue.py`: all tests pass.

## Dependencies
- Depends on: Task 1 — Authenticate tracker calls with the service-account token via the gateway, and expose a positive auth check

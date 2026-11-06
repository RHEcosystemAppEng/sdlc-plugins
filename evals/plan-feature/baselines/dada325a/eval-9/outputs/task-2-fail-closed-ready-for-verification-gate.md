# Task 2 — Gate verification on "Ready for Verification" and fail closed on unauthenticated empty searches

**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9008)
**Fix Versions:** (omitted — Feature has none)
**Parent Epic:** TC-9008: Fail-closed verification gate

## Repository
release-verifier

## Target Branch
main

## Description
Before running the expensive verification suite, the release verifier must look up the tracker issue linked to the pull request and verify only pull requests whose linked issue is in the "Ready for Verification" state; pull requests with no matching issue are skipped (TC-9008, requirements 1 and 2).

The Feature's Known Risks describe a fail-open path in exactly this gate: the tracker gateway answers an unauthenticated or under-privileged search with a successful empty result, `search_issues` exits 0 with `[]`, and `resolve_gated_issue` treats that as a normal "no matching issue" skip — so a run can finish green without ever verifying the pull request. This task makes the gate fail closed: an empty result is a legitimate skip only when the tracker session has been positively proven authenticated (using the authentication proof added in Task 1). Otherwise the gate errors out with a non-zero, auth-specific outcome instead of skipping.

## Files to Modify
- `src/gate/resolve_issue.py` — in `resolve_gated_issue(pr_url)`: add the "Ready for Verification" state check, and guard the empty-result skip site with the authentication proof so unproven-auth empty results fail closed
- `tests/gate/test_resolve_issue.py` — tests for state gating, legitimate skip, and the fail-closed path

## Implementation Notes
- Skip site to guard: `src/gate/resolve_issue.py::resolve_gated_issue(pr_url)` currently calls `src/tracker/client.py::search_issues` and returns `None` (skip) when the result is empty. That `return None` on empty is the exact fail-open site named in the Feature's Known Risks.
- Required ordering in `resolve_gated_issue`:
  1. Call the tracker client's authentication proof (Task 1). If it raises `TrackerAuthNotProvenError` (or authentication otherwise cannot be confirmed), propagate it / exit with a dedicated non-zero "auth not proven" status — do NOT return `None`.
  2. Call `search_issues(jql)` for the issue linked to `pr_url`.
  3. If the result is empty and authentication was proven → return `None` (legitimate skip) and log "no linked tracker issue for <pr_url>; skipping verification".
  4. If a linked issue exists but its state is not "Ready for Verification" → return `None` and log the issue key and its actual state.
  5. If the linked issue is "Ready for Verification" → return the issue so verification runs.
- Do not "fix" the risk by treating every empty result as an error — that would break the acceptance criterion that unlinked pull requests are skipped. The distinguishing input is the positive authentication proof, not the emptiness of the result.
- Use a distinct exit status / exception type for "auth not proven" so `scripts/pre-verify.sh` (Task 3) can report it as an authentication failure rather than a generic error.
- Compare the "Ready for Verification" state by exact status name as returned by the tracker search response; keep the status name in one module-level constant.
- Operational note (supplementary only): the Feature suggests a live run after merge to confirm the token works. That may be done in addition, but it is NOT a substitute for the fail-closed acceptance criterion and test below.
- Constraints (docs/constraints.md): §2 commit rules — Conventional Commits, `Implements <task-key>` footer, `Assisted-by:` trailer; §3 PR rules — branch named after the task issue ID, `gh pr create --base main`, post PR link to the Jira task; §5 code change rules — scope changes to the files listed above (§5.1), inspect `resolve_gated_issue` before modifying (§5.2), reuse the client's search and auth proof rather than re-implementing HTTP calls (§5.4), trace the full gate data flow input → decision → exit status (§5.6), doc comments on every new test and given-when-then comments on non-trivial tests (§5.11, §5.12).

## Reuse Candidates
- `src/tracker/client.py::search_issues` — existing search used to find the linked issue; reuse as-is
- `src/tracker/client.py` authentication proof / `TrackerAuthNotProvenError` (added in Task 1) — the positive auth signal the guard depends on

## Acceptance Criteria
- [ ] A pull request linked to an issue in "Ready for Verification" state is returned by `resolve_gated_issue` and verification runs
- [ ] A pull request linked to an issue in any other state is skipped with a log message naming the issue and its state
- [ ] A pull request with no linked issue is skipped with a log message, only when the tracker session is proven authenticated
- [ ] Fail-closed: when the tracker session cannot be proven authenticated (e.g. the gateway returns a successful empty `[]` search to an unauthenticated or under-privileged request), `resolve_gated_issue` exits non-zero / raises an auth-specific error instead of treating the empty result as a "no matching issue" skip
- [ ] The run never reports green (skip or pass) for a pull request whose linked-issue lookup was not performed with proven authentication

## Test Requirements
- [ ] Test: linked issue in "Ready for Verification" → `resolve_gated_issue` returns the issue
- [ ] Test: linked issue in another state (e.g. "In Progress") → returns `None` and logs the state
- [ ] Test: authentication proven + `search_issues` returns `[]` → returns `None` (legitimate skip) and logs the skip
- [ ] Fail-closed test: mock the tracker gateway to return a successful empty `[]` search while the authentication proof fails (unauthenticated / under-privileged token) → assert `resolve_gated_issue` raises the auth-not-proven error / produces the non-zero auth exit status and does NOT return `None`
- [ ] Fail-closed test: missing service-account token → gate exits non-zero and verification is not reported as skipped

## Verification Commands
- `pytest tests/gate/test_resolve_issue.py` — all tests pass

## Dependencies
- Depends on: Task 1 — Authenticate tracker calls with the service-account token via the gateway and expose an authentication proof

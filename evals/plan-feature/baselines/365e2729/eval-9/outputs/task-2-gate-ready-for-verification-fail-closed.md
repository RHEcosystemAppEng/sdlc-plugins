# Task 2 — Gate verification on a "Ready for Verification" linked issue and fail closed on unauthenticated empty results

**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9008)
**Fix Versions:** (omitted — TC-9008 has none)

## Repository
release-verifier

## Target Branch
main

## Description
`resolve_gated_issue(pr_url)` in `src/gate/resolve_issue.py` looks up the tracker issue linked to a pull request via `search_issues` and returns `None` (skip) when the result is empty. TC-9008 requires verification to run only when the linked issue is in the "Ready for Verification" state, and to skip (with a log message) when no linked issue exists or it is in another state.

The feature's Known Risks state that the tracker gateway returns a successful empty response to unauthenticated or under-privileged requests, so the gate currently treats "no matching issue" as a normal skip and a verifier run can finish green without ever verifying the pull request. This task makes the gate the owner of that risk: an empty result is only treated as a skip when it came from a proven-authenticated tracker session (Task 1's `verify_authenticated()`); otherwise the gate fails closed.

## Files to Modify
- `src/gate/resolve_issue.py` — add the "Ready for Verification" state check with skip logging, and fail closed in `resolve_gated_issue` when the empty result cannot be proven authenticated
- `tests/gate/test_resolve_issue.py` — cover Ready / not-Ready / no-issue skip and the unauthenticated-empty fail-closed path

## Implementation Notes
- **Gate/skip site:** `src/gate/resolve_issue.py::resolve_gated_issue(pr_url)`, specifically the branch that currently returns `None` when `search_issues` returns an empty list. This is where the guard belongs:
  - Before returning `None` for an empty result, require that the tracker client has proven authentication (`client.verify_authenticated()` from Task 1 returned success). If it has not — or if `search_issues` raised `TrackerAuthError` — do **not** return `None`; raise/propagate a `GateError` (subclass or wrapper of `TrackerAuthError`) so the gate's entry point exits non-zero.
  - Never catch `TrackerAuthError` (or any broad `Exception`) and convert it to `None`/skip.
- **State filter:** when an issue is found, return it for verification only if its status is exactly "Ready for Verification"; for any other status, log `skipping verification: linked issue <key> is in state <status>` and return `None`. For a proven-authenticated empty result, log `skipping verification: no linked tracker issue for <pr_url>` and return `None`.
- Distinguish the three outcomes explicitly in the return contract (verify / skip / error) so the CLI entry point maps them to distinct exit codes: verify = 0 with issue key on stdout, skip = 0 with a skip marker, auth-unverified/error = non-zero. Task 3's wrapper relies on the non-zero exit.
- Reuse the existing `search_issues` call in `resolve_gated_issue`; do not add a second tracker client.
- Constraints (docs/constraints.md): Conventional Commits with Jira footer and `Assisted-by:` trailer (§2.1–2.3); branch named after task ID, `--base main`, PR link on Jira (§3.1–3.3); scope limited to listed files, inspect before modifying, no duplicated logic (§5.1–5.4); test doc comments and given-when-then for non-trivial tests (§5.11–5.12).

## Reuse Candidates
- `src/tracker/client.py::search_issues` — existing search used by the gate
- `src/tracker/client.py::verify_authenticated` — auth proof added in Task 1; the gate must consult it before treating empty as skip
- `tests/gate/test_resolve_issue.py` — existing gate test fixtures for mocking the tracker client

## Acceptance Criteria
- [ ] A pull request whose linked issue is in "Ready for Verification" is returned for verification.
- [ ] A pull request whose linked issue is in any other state is skipped with a log message naming the issue key and state.
- [ ] A pull request with no linked issue is skipped with a log message — **only** when the tracker session is proven authenticated.
- [ ] **Fail-closed:** when `search_issues` returns `[]` and the tracker source cannot be proven authenticated (or `search_issues` raises `TrackerAuthError`), `resolve_gated_issue` raises a gate error and the gate entry point exits non-zero, instead of returning `None` and treating the empty result as a skip.
- [ ] No code path in `resolve_gated_issue` converts an authentication error into a skip.

## Test Requirements
- [ ] Test: linked issue in "Ready for Verification" → issue returned for verification.
- [ ] Test: linked issue in another state (e.g. "In Progress") → `None` and skip log emitted.
- [ ] Test: authenticated client, empty search → `None` and "no linked tracker issue" skip log.
- [ ] **Fail-closed test:** mock the tracker client so `search_issues` returns `[]` and `verify_authenticated()` fails (simulating the gateway's unauthenticated 200/empty response); assert `resolve_gated_issue` raises the gate error (not `None`) and that the CLI entry point exits non-zero.
- [ ] **Fail-closed test:** mock `search_issues` to raise `TrackerAuthError`; assert the error propagates and the result is not a skip.

## Verification Commands
- `pytest tests/gate/test_resolve_issue.py` — all tests pass, including both fail-closed cases

## Dependencies
- Depends on: Task 1 — Authenticate tracker calls with the service-account token via the gateway and fail closed on unproven authentication

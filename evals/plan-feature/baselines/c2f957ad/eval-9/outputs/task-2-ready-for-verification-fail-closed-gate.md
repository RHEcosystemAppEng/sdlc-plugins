# Task 2 — Gate verification on a "Ready for Verification" linked issue; fail closed on unproven-auth empty search

**Summary**: TC-9008: Gate verification on Ready for Verification linked issue and fail closed on unauthenticated empty search
**Issue type**: Task | **Labels**: ai-generated-jira | **Priority**: Major (inherited) | **fixVersions**: omitted (Feature has none)
**Links**: TC-9008 incorporates this task; depends on Task 1

---

## Repository
release-verifier

## Target Branch
main

## Description
Before the expensive verification suite runs, the gate must find the tracker issue linked to the pull request and allow verification only when that issue is in the "Ready for Verification" state (TC-9008, requirements 1 and 2). PRs with no linked issue, or whose linked issue is in another state, are skipped with a log message.

The Feature's Known Risks name a fail-open path: the tracker gateway returns a successful empty `[]` to unauthenticated or under-privileged requests, and `resolve_gated_issue` treats an empty result as a normal "no matching issue" skip. A verifier run can then finish green without verifying the PR. This task owns that skip site. It must make the gate **fail closed**: an empty result may count as a skip only after authentication has been proven.

## Files to Modify
- `src/gate/resolve_issue.py` — add the "Ready for Verification" state check with skip logging, and guard the empty-result skip with the Task 1 auth proof so an unproven-auth empty result raises instead of returning `None`
- `tests/gate/test_resolve_issue.py` — add tests for the Ready, non-Ready, authenticated-empty and unauthenticated-empty paths

## Implementation Notes
- **Gate and skip site**: `src/gate/resolve_issue.py::resolve_gated_issue(pr_url)` calls `search_issues` and currently returns `None` (skip) when the result is empty. The fail-closed guard belongs here, on the empty-result branch.
- **Fail-closed guard**: when `search_issues` returns `[]`, call the Task 1 auth proof in `src/tracker/client.py` (for example `verify_authenticated()`) before returning the skip value.
  - If the auth proof raises `TrackerAuthError`, or authentication cannot otherwise be proven, let the error propagate (or re-raise a gate-specific error) so the gate exits non-zero.
  - Never convert it to `None` or a skip.
  - Never catch `TrackerAuthError` broadly and log-and-continue.
  - You may run the auth proof once before the search instead. Either way, an empty result must never become a skip without proven auth.
- **State gating**: when a linked issue is found, compare its status to "Ready for Verification". Keep the status string in a single module-level constant, not inline literals.
  - Ready → return the issue (verify).
  - Any other status → return the skip value and log the PR URL, issue key and actual status.
  - Proven-auth empty result → skip and log "no linked issue".
- Make the three outcomes distinct so the wrapper (Task 3) can tell them apart: verify, skip, and error (non-zero exit). For example, keep `None`/skip for legitimate skips and an exception or non-zero exit code for errors.
- Reuse the existing search: build the JQL in the existing `resolve_gated_issue` flow and call the existing `src/tracker/client.py::search_issues`. Do not add a second search client (requirement notes: "Uses the existing search client").
- A post-merge live run confirming the token works is a supplementary check only. The tests below are the required coverage for this risk.
- Constraints (docs/constraints.md):
  - §1.4/§5.1: keep changes to the listed files.
  - §5.2: inspect before editing.
  - §5.4: reuse `search_issues`.
  - §5.6: trace PR URL → search → auth proof → verify/skip/error.
  - §5.9–5.13: test doc comments and given-when-then comments for non-trivial tests.
  - §2.1–2.3: commit rules.
  - §3.1–3.3: PR rules.

## Reuse Candidates
- `src/tracker/client.py::search_issues` — the existing search client for finding the linked issue
- `src/tracker/client.py` auth proof (added in Task 1) — the fail-closed check to call before treating `[]` as a skip
- `tests/gate/test_resolve_issue.py` — follow the existing gate test structure and the way it mocks `search_issues`

## Acceptance Criteria
- [ ] A PR linked to an issue in the "Ready for Verification" state is returned for verification.
- [ ] A PR linked to an issue in any other state is skipped, and a log message names the PR, the issue key and the actual state.
- [ ] A PR with no linked issue is skipped with a log message **only when** the tracker auth proof succeeds.
- [ ] **Fail-closed**: when `search_issues` returns `[]` and authentication cannot be proven (the auth proof raises `TrackerAuthError` or the request is unauthenticated or under-privileged), `resolve_gated_issue` raises and the gate exits non-zero. It does not return `None` or skip.
- [ ] Tracker lookups reuse the existing `search_issues` client.

## Test Requirements
- [ ] A test asserts a linked issue in "Ready for Verification" is returned for verification.
- [ ] A test asserts a linked issue in another state (for example "In Progress") is skipped and the skip is logged.
- [ ] A test asserts that `search_issues` returning `[]` while the auth proof succeeds leads to a logged skip.
- [ ] **Fail-closed test**: mock `search_issues` to return `[]` (exit 0) and the auth proof to raise `TrackerAuthError`, simulating the gateway's successful-empty response to an unauthenticated request. Assert `resolve_gated_issue` raises (non-zero exit) and does **not** return `None`.
- [ ] **Fail-closed test (under-privileged)**: same as above, but the auth proof reports an authenticated principal without search permission. Assert the gate raises and exits non-zero.

## Verification Commands
- `pytest tests/gate/test_resolve_issue.py` — all tests pass

## Dependencies
- Depends on: Task 1 — Authenticate tracker calls with the service-account token via the API gateway

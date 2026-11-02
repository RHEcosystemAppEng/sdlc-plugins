## Repository
release-verifier

## Target Branch
main

## Description
Implement the full gated verification flow: search the tracker for the issue linked to the pull request, run verification only when the linked issue is in the "Ready for Verification" state, and skip with a log message otherwise. This builds on the fail-closed gate from Task 2 to complete the feature's core verification gating logic.

## Files to Modify
- `src/gate/resolve_issue.py` — add state checking logic to `resolve_gated_issue` so that only issues in "Ready for Verification" state trigger verification; issues in other states cause a skip with a log message
- `tests/gate/test_resolve_issue.py` — add tests for state-based gating

## Implementation Notes
- `src/gate/resolve_issue.py` currently returns `None` (skip) or the matching issue. Extend the logic: when a matching issue is found, check its status field. If status is "Ready for Verification", return the issue (proceed with verification). If status is anything else, log a skip message and return `None`.
- The status field name and values come from the tracker API response. Check `src/tracker/client.py` for the response shape returned by `search_issues`.
- Per docs/constraints.md §5 (Code Change Rules): keep changes scoped to the state-checking logic; the fail-closed guard is handled in Task 2.

## Acceptance Criteria
- [ ] Pull requests linked to an issue in "Ready for Verification" state are verified
- [ ] Pull requests linked to an issue in any other state are skipped with a descriptive log message
- [ ] Pull requests with no linked issue are handled by the existing skip/fail-closed logic (no regression)

## Test Requirements
- [ ] Test that `resolve_gated_issue` returns the issue when the linked issue is in "Ready for Verification" state
- [ ] Test that `resolve_gated_issue` returns `None` (skip) when the linked issue is in a different state (e.g., "In Progress", "Done")
- [ ] Test that the skip log message includes the issue key and current state

## Dependencies
- Depends on: Task 2 — Fail-closed gate (state checking builds on the fail-closed guard)

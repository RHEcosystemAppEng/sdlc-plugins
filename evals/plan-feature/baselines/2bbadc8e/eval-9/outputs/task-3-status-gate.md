## Repository
release-verifier

## Target Branch
main

## Description
Gate the verification suite on the linked tracker issue's status. After resolving the linked issue, check whether its status is "Ready for Verification". If the issue exists but is not in that status, skip verification with a log message. If the issue is in the correct status, proceed with the verification suite.

## Files to Modify
- `src/gate/resolve_issue.py` — extend `resolve_gated_issue` (or add a downstream check) to inspect the resolved issue's status field and only allow verification when the status is "Ready for Verification"
- `tests/gate/test_resolve_issue.py` — add tests for the status-based gating logic

## Implementation Notes
- `src/gate/resolve_issue.py` currently resolves the linked issue and returns it (or `None` for skip). After Task 2's fail-closed guard validates the response, the status check should be applied to the resolved issue object. If the issue's status is not "Ready for Verification", return `None` with a log message explaining the skip reason (e.g., "Issue TC-100 is in status 'In Progress', skipping verification").
- Ensure the status comparison is exact (case-sensitive match against "Ready for Verification") to avoid false matches on similar status names.
- The skip-due-to-status path is a legitimate skip (the issue exists and was found via an authenticated request), distinct from the fail-closed empty-response path handled by Task 2.
- Per docs/constraints.md section 2 (Commit Rules): every commit must reference TC-9008 in the footer and follow Conventional Commits format.
- Per docs/constraints.md section 3 (PR Rules): the feature branch must be named after the Jira issue ID.

## Acceptance Criteria
- [ ] Pull requests linked to a tracker issue in "Ready for Verification" status proceed to verification
- [ ] Pull requests linked to a tracker issue in any other status are skipped with a log message stating the issue key and current status
- [ ] Pull requests with no linked issue are skipped (existing behavior, preserved by Task 2's fail-closed guard for authenticated empty responses)

## Test Requirements
- [ ] Test that verification proceeds when the linked issue has status "Ready for Verification"
- [ ] Test that verification is skipped with a log message when the linked issue has a different status (e.g., "In Progress", "Done")
- [ ] Test that the skip log message includes the issue key and the current status value
- [ ] Test that the status comparison is exact (e.g., "ready for verification" in lowercase does not match)

## Dependencies
- Depends on: Task 2 — Add fail-closed guard against silent empty responses in the issue gate

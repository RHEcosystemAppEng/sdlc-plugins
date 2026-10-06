## Repository
trustify-ui

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9006` into `main`. The PR description should summarize all changes made across the feature's tasks for the vulnerability remediation tracking dashboard, including:
- Backend: three new remediation API endpoints (summary, by-product, export) with aggregation service and integration tests
- Frontend: new remediation dashboard page with summary cards, progress chart, filterable vulnerability table, and CSV export button
- Documentation: user guide and API reference for the remediation feature

## Acceptance Criteria
- [ ] A PR from `TC-9006` to `main` is open and ready for review

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR

## Dependencies
- Depends on: Task 2 — Add remediation summary aggregation service and endpoint
- Depends on: Task 3 — Add per-product remediation breakdown endpoint
- Depends on: Task 4 — Add CSV export endpoint for remediation report
- Depends on: Task 5 — Add API client functions, types, and React Query hooks for remediation endpoints
- Depends on: Task 6 — Add remediation dashboard page with summary cards and progress chart
- Depends on: Task 7 — Add filterable vulnerability table to remediation dashboard
- Depends on: Task 8 — Add CSV export button to remediation dashboard
- Depends on: Task 9 — Document remediation dashboard and aggregation endpoints

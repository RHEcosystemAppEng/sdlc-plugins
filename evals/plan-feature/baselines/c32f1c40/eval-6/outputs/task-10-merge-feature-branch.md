## Repository
trustify-ui

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9006` into `main`. The PR description should summarize all changes made across the feature's tasks, including: backend remediation aggregation service and REST endpoints, frontend remediation dashboard with summary cards, progress chart, and filterable vulnerability table, tests across both repositories, and documentation.

## Acceptance Criteria
- [ ] A PR from `TC-9006` to `main` is open and ready for review
- [ ] PR description summarizes all changes from Tasks 2-9
- [ ] All CI checks pass on the PR

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2-9) have been merged into the feature branch before creating the merge PR
- [ ] Verify no merge conflicts exist between TC-9006 and main

## Dependencies
- Depends on: Task 2 -- Add remediation data models and aggregation service
- Depends on: Task 3 -- Add remediation summary and by-product REST endpoints
- Depends on: Task 4 -- Add remediation endpoint integration tests
- Depends on: Task 5 -- Add remediation API types, client functions, and React Query hooks
- Depends on: Task 6 -- Create remediation dashboard page with summary cards and progress chart
- Depends on: Task 7 -- Add filterable vulnerability table to remediation dashboard
- Depends on: Task 8 -- Add remediation dashboard unit and E2E tests
- Depends on: Task 9 -- Document remediation dashboard and aggregation endpoints

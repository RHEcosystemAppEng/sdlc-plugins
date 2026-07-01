# Task 9 — Merge feature branch TC-9003 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: new SBOM comparison diff model, comparison service and endpoint, frontend API layer, comparison page UI, SBOM list page selection integration, MSW mocks, and integration tests.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR

## Dependencies
- Depends on: Task 2 — Add SBOM comparison diff model structs
- Depends on: Task 3 — Add SBOM comparison service and endpoint
- Depends on: Task 4 — Add frontend API types, client function, and React Query hook for SBOM comparison
- Depends on: Task 5 — Add SBOM comparison page with header toolbar and diff sections
- Depends on: Task 6 — Add SBOM selection checkboxes and "Compare selected" action to SbomListPage
- Depends on: Task 7 — Add MSW handlers and mock fixtures for SBOM comparison endpoint
- Depends on: Task 8 — Add integration tests for the SBOM comparison endpoint

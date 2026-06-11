# Task 10 — Merge feature branch TC-9003 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: new SBOM comparison model structs, comparison service logic, REST endpoint, frontend API layer, comparison page UI with diff sections, SBOM list selection integration, MSW test fixtures, and integration tests.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR

## Dependencies
- Depends on: Task 2 — Add SBOM comparison model structs
- Depends on: Task 3 — Add SBOM comparison service logic
- Depends on: Task 4 — Add GET /api/v2/sbom/compare endpoint
- Depends on: Task 5 — Add frontend API types, client function, and React Query hook for SBOM comparison
- Depends on: Task 6 — Add SBOM comparison page with diff sections
- Depends on: Task 7 — Add SBOM selection and "Compare selected" to SbomListPage
- Depends on: Task 8 — Add MSW mock handlers and test fixtures for SBOM comparison
- Depends on: Task 9 — Add integration tests for the SBOM comparison endpoint

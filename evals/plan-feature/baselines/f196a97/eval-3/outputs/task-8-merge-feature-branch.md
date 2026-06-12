# Task 8 — Merge feature branch TC-9003 to main

## Repository
trustify-ui

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: the new SBOM comparison backend endpoint, the frontend comparison page with SBOM selectors and diff sections, the SBOM list page selection enhancement, and the E2E test coverage.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR

## Dependencies
- Depends on: Task 2 — Add SBOM comparison diff model and service logic
- Depends on: Task 3 — Add GET /api/v2/sbom/compare endpoint
- Depends on: Task 4 — Add comparison API types, client function, and React Query hook
- Depends on: Task 5 — Add SBOM comparison page with diff sections
- Depends on: Task 6 — Add SBOM selection and "Compare selected" action to SbomListPage
- Depends on: Task 7 — Add Playwright E2E test for SBOM comparison workflow

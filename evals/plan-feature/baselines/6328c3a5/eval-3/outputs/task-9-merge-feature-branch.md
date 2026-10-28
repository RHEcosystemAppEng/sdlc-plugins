## Repository
trustify-ui

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main` in the trustify-ui repository. The PR description should summarize all changes made across the feature's tasks, including the new SBOM comparison page, API integration, SBOM list selection, and export functionality.

Since this is a cross-repo feature, the trustify-backend feature branch `TC-9003` should also be merged to `main` via a separate PR in that repository.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review in trustify-ui
- [ ] A PR from `TC-9003` to `main` is open and ready for review in trustify-backend
- [ ] PR descriptions summarize all changes made across the feature's tasks

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify all tests pass on the feature branch before creating the merge PR

## Dependencies
- Depends on: Task 2 — Implement SBOM comparison service and model
- Depends on: Task 3 — Create SBOM comparison REST endpoint with integration tests
- Depends on: Task 4 — Add SBOM comparison API client, types, and React Query hook
- Depends on: Task 5 — Create SBOM comparison page with diff sections
- Depends on: Task 6 — Add SBOM comparison selection to SBOM list page
- Depends on: Task 7 — Add export functionality for SBOM comparison diff
- Depends on: Task 8 — SBOM comparison documentation

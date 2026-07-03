## Repository
trustify-ui

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks:

- **Backend (trustify-backend):** New `GET /api/v2/sbom/compare` endpoint with comparison model types, service logic, and integration tests
- **Frontend (trustify-ui):** New SBOM comparison page at `/sbom/compare` with header toolbar, six collapsible diff sections, SBOM list page selection integration, export as JSON/CSV, and comprehensive test coverage
- **Documentation:** New API reference and user guide for the comparison feature

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review
- [ ] PR description summarizes all changes across backend, frontend, and documentation

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify CI passes on the feature branch before opening the PR

## Dependencies
- Depends on: Task 2 -- Add SBOM comparison response model types
- Depends on: Task 3 -- Add SBOM comparison service and REST endpoint
- Depends on: Task 4 -- Add SBOM comparison integration tests
- Depends on: Task 5 -- Add SBOM comparison API types and React Query hook
- Depends on: Task 6 -- Implement SBOM comparison page with diff sections
- Depends on: Task 7 -- Add comparison selection to SBOM list page
- Depends on: Task 8 -- Implement comparison diff export as JSON and CSV
- Depends on: Task 9 -- Add comparison page tests and mock fixtures
- Depends on: Task 10 -- Document SBOM comparison endpoint and UI

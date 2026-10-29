## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: the backend SBOM comparison model, service, and endpoint (trustify-backend), and the frontend comparison page with API client, diff sections, and export functionality (trustify-ui).

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review
- [ ] The PR description summarizes all changes from Tasks 2-6

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify CI passes on the feature branch before creating the merge PR

## Dependencies
- Depends on: Task 2 — Add SBOM comparison model and diff service
- Depends on: Task 3 — Add SBOM comparison REST endpoint with integration tests
- Depends on: Task 4 — Add API client and React Query hook for SBOM comparison
- Depends on: Task 5 — Create SBOM comparison page with diff sections
- Depends on: Task 6 — Add diff export for SBOM comparison

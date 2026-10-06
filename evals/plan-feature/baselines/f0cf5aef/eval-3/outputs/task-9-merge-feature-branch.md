## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks, covering the backend comparison engine (model, service, endpoint, tests) and the frontend comparison UI (API types, page component, route integration, tests, documentation).

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review in trustify-backend
- [ ] A PR from `TC-9003` to `main` is open and ready for review in trustify-ui
- [ ] PR descriptions summarize all changes made across the feature's tasks

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify all backend integration tests pass on the feature branch
- [ ] Verify all frontend unit and E2E tests pass on the feature branch

## Dependencies
- Depends on: Task 2 — Add SBOM comparison model and diff service
- Depends on: Task 3 — Add SBOM comparison endpoint with integration tests
- Depends on: Task 4 — Add comparison API types, client function, and React Query hook
- Depends on: Task 5 — Add SBOM comparison page with diff sections
- Depends on: Task 6 — Add comparison route and SBOM list page compare action
- Depends on: Task 7 — Add comparison page unit and E2E tests
- Depends on: Task 8 — Document comparison endpoint and comparison UI workflow

## Repository
trustify-ui

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks, including the backend comparison API (model, service, endpoint) and the frontend comparison UI (API types, comparison page, SBOM selection, routing, documentation).

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review
- [ ] PR description summarizes all changes from Tasks 2-7

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR

## Dependencies
- Depends on: Task 2 — Add SBOM comparison model and diff service
- Depends on: Task 3 — Add comparison endpoint and integration tests
- Depends on: Task 4 — Add comparison API types, client function, and React Query hook
- Depends on: Task 5 — Add SBOM comparison page with diff sections
- Depends on: Task 6 — Add SBOM selection on list page and route wiring
- Depends on: Task 7 — Document comparison endpoint and UI

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks:

- Backend: new SBOM comparison model, service, and `GET /api/v2/sbom/compare` endpoint with integration tests
- Frontend: comparison API types and hook, full comparison page at `/sbom/compare` with SBOM selectors, collapsible diff sections, URL-shareable state, and export functionality
- Documentation: new endpoint reference and UI workflow guide

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review
- [ ] PR description summarizes all changes from Tasks 2-6
- [ ] All CI checks pass on the PR

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch `TC-9003` before creating the merge PR
- [ ] Verify the feature branch is up to date with `main` (rebase or merge main into the feature branch if needed)

## Dependencies
- Depends on: Task 2 — Backend comparison model and service logic
- Depends on: Task 3 — Backend comparison endpoint and integration tests
- Depends on: Task 4 — Frontend comparison API layer
- Depends on: Task 5 — Frontend comparison page
- Depends on: Task 6 — Documentation

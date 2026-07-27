# Task 9: Merge feature branch TC-9003 to main

**Summary**: Merge feature branch TC-9003 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks:

- Backend: new SBOM comparison model, diff service, and `GET /api/v2/sbom/compare` endpoint with integration tests
- Frontend: new SbomComparePage with header toolbar, six diff sections, URL-shareable comparisons, and comprehensive unit/E2E tests
- Documentation: new API endpoint reference and UI workflow guide

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review
- [ ] The PR description summarizes all changes from Tasks 2-8
- [ ] All CI checks pass on the PR

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify all backend integration tests pass on the feature branch
- [ ] Verify all frontend unit and E2E tests pass on the feature branch

## Dependencies
- Depends on: Task 2 — Add SBOM comparison model and diff service
- Depends on: Task 3 — Add comparison endpoint with integration tests
- Depends on: Task 4 — Add comparison API types and React Query hook
- Depends on: Task 5 — Add SbomComparePage with diff sections UI
- Depends on: Task 6 — Add comparison route and SbomListPage multi-select
- Depends on: Task 7 — Add frontend tests for SbomComparePage
- Depends on: Task 8 — Documentation for SBOM comparison feature

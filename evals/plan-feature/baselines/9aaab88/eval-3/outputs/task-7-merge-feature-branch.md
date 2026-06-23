## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Merge the TC-9003 feature branch back into `main` in both trustify-backend and trustify-ui repositories. This finalizes the SBOM Comparison View feature, making the backend endpoint and frontend UI available in production.

## Acceptance Criteria
- [ ] Feature branch `TC-9003` is merged into `main` in trustify-backend
- [ ] Feature branch `TC-9003` is merged into `main` in trustify-ui
- [ ] All CI checks pass on the merge commits
- [ ] Feature branch is deleted after successful merge in both repositories

## Test Requirements
- [ ] Verify all integration tests pass on `main` after merge in trustify-backend
- [ ] Verify all unit and E2E tests pass on `main` after merge in trustify-ui
- [ ] Verify the comparison endpoint is accessible from the merged `main` branch

## Dependencies
- Depends on: Task 2 — Backend comparison models
- Depends on: Task 3 — Backend comparison service and endpoint
- Depends on: Task 4 — Frontend API types and hook
- Depends on: Task 5 — Frontend comparison page
- Depends on: Task 6 — Frontend SBOM list selection

sha256-md:b7ef327379e44718f50784a9a0229c8b8fe514a30ef73e8b5fd52bff19a7a089

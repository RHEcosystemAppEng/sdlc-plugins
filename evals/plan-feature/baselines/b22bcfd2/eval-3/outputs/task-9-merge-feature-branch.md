## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Merge the TC-9003 feature branch back to main in both trustify-backend and trustify-ui repositories. This finalizes the SBOM comparison view feature, making all backend and frontend changes available together.

## Acceptance Criteria
- [ ] TC-9003 feature branch is merged to main in trustify-backend
- [ ] TC-9003 feature branch is merged to main in trustify-ui
- [ ] All CI checks pass on the merged main branches
- [ ] Feature branch is cleaned up after merge

## Test Requirements
- [ ] All existing tests continue to pass on main after merge
- [ ] New comparison endpoint tests pass on main
- [ ] New frontend comparison page tests pass on main

## Dependencies
- Depends on: Task 2 — Backend comparison model
- Depends on: Task 3 — Backend comparison service
- Depends on: Task 4 — Backend comparison endpoint
- Depends on: Task 5 — Backend integration tests
- Depends on: Task 6 — Frontend API types and hooks
- Depends on: Task 7 — Frontend comparison page
- Depends on: Task 8 — Frontend tests

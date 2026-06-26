## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Merge the feature branch `TC-9003` to `main` in both `trustify-backend` and `trustify-ui` after all SBOM comparison view tasks are complete and verified. This closes the feature branch and makes the comparison endpoint and UI available in the main development line.

## Acceptance Criteria
- [ ] All intermediate tasks (2-6) are complete and verified
- [ ] Branch `TC-9003` is merged to `main` in `trustify-backend`
- [ ] Branch `TC-9003` is merged to `main` in `trustify-ui`
- [ ] No merge conflicts remain
- [ ] CI passes on `main` after merge in both repositories

## Dependencies
- Depends on: Task 2 -- Implement SBOM comparison model and service
- Depends on: Task 3 -- Implement comparison endpoint and integration tests
- Depends on: Task 4 -- Add API types, client function, and React Query hook
- Depends on: Task 5 -- Implement SBOM comparison page UI
- Depends on: Task 6 -- Add tests for comparison page

[sdlc-workflow] Description digest: sha256-md:a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9

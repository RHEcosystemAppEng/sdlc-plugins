## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Merge the `TC-9003` feature branch back into `main` after all backend and frontend tasks are complete. This consolidates the SBOM comparison endpoint, service, models, and the frontend comparison UI into the main branch for release.

## Acceptance Criteria
- [ ] All intermediate tasks (Tasks 2-10) are complete and merged to `TC-9003`
- [ ] CI passes on the feature branch
- [ ] Feature branch `TC-9003` is merged to `main` via pull request
- [ ] No merge conflicts

## Test Requirements
- [ ] All backend integration tests pass on the merged branch
- [ ] All frontend unit and E2E tests pass on the merged branch
- [ ] No regressions in existing test suites

## Dependencies
- Depends on: Task 2 — Backend comparison model structs
- Depends on: Task 3 — Backend comparison service
- Depends on: Task 4 — Backend comparison endpoint
- Depends on: Task 5 — Backend integration tests
- Depends on: Task 6 — Frontend API types and client function
- Depends on: Task 7 — Frontend comparison hook
- Depends on: Task 8 — Frontend comparison page
- Depends on: Task 9 — Frontend SBOM list selection
- Depends on: Task 10 — Frontend E2E and MSW mocks

[sdlc-workflow] Description digest: sha256-md:157f39d7d7ebdfbf174ad7077a6ad6fdc2ddb6cc71bd000d90a2666f4c9b3c9a

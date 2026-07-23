## Repository
trustify-ui

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks for the SBOM comparison view:
- Backend: new comparison model, diff service, and GET /api/v2/sbom/compare endpoint with integration tests
- Frontend: comparison API types, React Query hook, SbomComparePage with header toolbar and six collapsible diff sections, /sbom/compare route, SbomListPage "Compare selected" integration, unit tests, MSW mocks, and E2E tests
- Documentation: endpoint reference and UI workflow guide

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review
- [ ] PR description summarizes all changes made across the SBOM comparison feature tasks
- [ ] All CI checks pass on the PR

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the TC-9003 feature branch before creating the merge PR
- [ ] Verify the feature branch builds and all tests pass before opening the PR

## Dependencies
- Depends on: Task 2 -- Backend: Add SBOM comparison model and diff service
- Depends on: Task 3 -- Backend: Add SBOM comparison endpoint and integration tests
- Depends on: Task 4 -- Frontend: Add comparison API types, client function, and React Query hook
- Depends on: Task 5 -- Frontend: Build SBOM comparison page with diff sections
- Depends on: Task 6 -- Frontend: Add comparison route and SBOM list page selection
- Depends on: Task 7 -- Frontend: Add tests for SBOM comparison feature
- Depends on: Task 8 -- Documentation: Document comparison endpoint and UI

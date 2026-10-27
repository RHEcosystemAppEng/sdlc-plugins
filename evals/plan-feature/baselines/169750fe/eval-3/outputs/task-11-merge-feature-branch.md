## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: new SBOM comparison backend endpoint, frontend comparison page with PatternFly UI, SBOM list page selection capability, and supporting tests and documentation.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review
- [ ] PR description summarizes all changes across backend and frontend
- [ ] All CI checks pass on the PR

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Backend integration tests pass on the feature branch
- [ ] Frontend component tests pass on the feature branch

## Dependencies
- Depends on: Task 2 — Backend comparison model
- Depends on: Task 3 — Backend comparison service
- Depends on: Task 4 — Backend comparison endpoint
- Depends on: Task 5 — Backend integration tests
- Depends on: Task 6 — Frontend API types and client
- Depends on: Task 7 — Frontend comparison page
- Depends on: Task 8 — Frontend MSW mocks
- Depends on: Task 9 — Frontend SBOM list compare action
- Depends on: Task 10 — Documentation

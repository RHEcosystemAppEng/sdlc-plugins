## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: the backend SBOM comparison diff service and REST endpoint, the frontend comparison page with diff sections and export, the SBOM list page selection UI, and the feature documentation.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review
- [ ] PR description summarizes all changes from Tasks 2-7
- [ ] All CI checks pass on the PR

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify the feature branch is up to date with `main` (rebase or merge main into feature branch if needed)

## Dependencies
- Depends on: Task 2 — Add SBOM comparison model and diff service
- Depends on: Task 3 — Add SBOM comparison REST endpoint with integration tests
- Depends on: Task 4 — Add SBOM comparison API types, client function, and hook
- Depends on: Task 5 — Add SBOM comparison page with diff sections and export
- Depends on: Task 6 — Add SBOM selection and compare navigation to list page
- Depends on: Task 7 — Document SBOM comparison endpoint and UI

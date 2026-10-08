## Repository
trustify-ui

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: the backend SBOM comparison endpoint (model, service, REST handler), the frontend comparison page UI (API types, React Query hook, comparison page with PatternFly diff sections, SBOM list selection), and the documentation for the new comparison feature.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review
- [ ] PR description summarizes all changes from Tasks 2-7
- [ ] All CI checks pass on the PR

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2-7) have been merged into the feature branch `TC-9003` before creating the merge PR
- [ ] Verify the feature branch is up to date with `main` (rebase or merge main into feature branch if needed)

## Dependencies
- Depends on: Task 2 -- Add SBOM comparison model types and diff service
- Depends on: Task 3 -- Add SBOM comparison endpoint with integration tests
- Depends on: Task 4 -- Add SBOM comparison API types, client function, and React Query hook
- Depends on: Task 5 -- Implement SBOM comparison page with diff sections
- Depends on: Task 6 -- Add SBOM comparison selection to list page
- Depends on: Task 7 -- Document SBOM comparison endpoint and UI

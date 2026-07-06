## Repository
trustify-ui

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: backend SBOM comparison models, service, and endpoint; frontend API types, client, hook, comparison page with diff sections, and SBOM list page compare workflow; and documentation updates.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review
- [ ] The PR description summarizes all changes across backend and frontend

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR

## Dependencies
- Depends on: Task 2 -- Add SBOM comparison model types
- Depends on: Task 3 -- Add SBOM comparison service and endpoint with integration tests
- Depends on: Task 4 -- Add SBOM comparison API types, client function, and React Query hook
- Depends on: Task 5 -- Add SBOM comparison page with header toolbar and diff sections
- Depends on: Task 6 -- Add compare workflow to SBOM list page and route registration
- Depends on: Task 7 -- Document SBOM comparison endpoint and UI

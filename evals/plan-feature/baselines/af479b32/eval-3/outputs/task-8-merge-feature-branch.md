## Repository
trustify-ui

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: the backend SBOM comparison endpoint, the frontend comparison page with diff sections, the SBOM list page comparison integration, and the documentation updates. This PR represents the complete SBOM comparison view feature (TC-9003) ready for final review.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review
- [ ] PR description summarizes all changes from Tasks 2-7
- [ ] All CI checks pass on the feature branch

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify the feature branch builds successfully with all changes integrated
- [ ] Verify no merge conflicts with `main`

## Dependencies
- Depends on: Task 2 -- Add SBOM comparison model and diff service
- Depends on: Task 3 -- Add SBOM comparison endpoint and integration tests
- Depends on: Task 4 -- Add comparison API types, client function, and React Query hook
- Depends on: Task 5 -- Create SBOM comparison page with diff sections
- Depends on: Task 6 -- Add comparison selection to SBOM list page
- Depends on: Task 7 -- Document SBOM comparison endpoint and UI workflow

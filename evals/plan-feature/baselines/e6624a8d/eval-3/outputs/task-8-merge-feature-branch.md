## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: backend SBOM comparison models, service, and endpoint; frontend API types, React Query hook, comparison page with Figma-aligned diff sections, route registration, and SBOM list page integration; and documentation updates. This completes the coordinated delivery of the SBOM comparison view feature.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review
- [ ] PR description summarizes all changes across all intermediate tasks
- [ ] All CI checks pass on the PR

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify no merge conflicts exist between `TC-9003` and `main`

## Dependencies
- Depends on: Task 2 -- Add SBOM comparison diff models and service
- Depends on: Task 3 -- Add SBOM comparison REST endpoint with integration tests
- Depends on: Task 4 -- Add comparison API types, client function, and React Query hook
- Depends on: Task 5 -- Implement SBOM comparison page with diff sections
- Depends on: Task 6 -- Add comparison route and SBOM list page selection integration
- Depends on: Task 7 -- Document SBOM comparison endpoint and UI

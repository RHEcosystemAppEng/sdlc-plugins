## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: backend SBOM comparison service and endpoint, frontend comparison page and SBOM list page multi-select, and documentation updates. This PR represents the coordinated delivery of the complete SBOM comparison view feature.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review
- [ ] PR description summarizes all changes: comparison model/service, endpoint, API types/hooks, comparison page, list page modifications, and documentation
- [ ] All intermediate task PRs have been merged into the feature branch before this PR is created

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2-8) have been merged into the `TC-9003` feature branch before creating the merge PR
- [ ] Verify no merge conflicts exist between `TC-9003` and `main`

## Dependencies
- Depends on: Task 2 — Add SBOM comparison model and diff service
- Depends on: Task 3 — Add GET /api/v2/sbom/compare endpoint
- Depends on: Task 4 — Add integration tests for SBOM comparison endpoint
- Depends on: Task 5 — Add comparison API types, client function, and React Query hook
- Depends on: Task 6 — Add SBOM comparison page with diff sections
- Depends on: Task 7 — Add SBOM multi-select and comparison navigation on list page
- Depends on: Task 8 — Document SBOM comparison endpoint and UI

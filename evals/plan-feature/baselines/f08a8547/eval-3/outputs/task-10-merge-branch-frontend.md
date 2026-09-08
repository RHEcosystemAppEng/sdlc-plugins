## Repository
trustify-ui

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main` in the trustify-ui repository. The PR description should summarize all frontend changes made across the feature's tasks: the SBOM comparison API types and hook, the comparison page UI with diff sections, the route registration, and the SbomListPage integration.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open in the trustify-ui repository and ready for review
- [ ] PR description summarizes all frontend changes: API types/hook, comparison page, route, list page integration
- [ ] All intermediate frontend task PRs have been merged into the TC-9003 feature branch

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 5, 6, 7) have been merged into the feature branch before creating the merge PR
- [ ] Verify the feature branch builds and all tests pass before opening the PR

## Dependencies
- Depends on: Task 5 — Add SBOM comparison API types, client function, and React Query hook
- Depends on: Task 6 — Build SBOM comparison page with diff sections
- Depends on: Task 7 — Add SBOM comparison route and SbomListPage integration

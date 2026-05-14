# Task 6 — Merge feature branch TC-9003 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create PRs to merge feature branch `TC-9003` into `main` for both trustify-backend and trustify-ui repositories. The PR descriptions should summarize all changes made across the feature's tasks: the new SBOM comparison diff endpoint in the backend, and the comparison page with SBOM list selection support in the frontend.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review in trustify-backend
- [ ] A PR from `TC-9003` to `main` is open and ready for review in trustify-ui
- [ ] PR descriptions summarize all changes from Tasks 2-5

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2, 3, 4, 5) have been merged into the feature branch before creating the merge PRs
- [ ] Verify CI passes on the merge PRs

## Dependencies
- Depends on: Task 2 — Add SBOM comparison diff endpoint
- Depends on: Task 3 — Add SBOM multi-select and "Compare selected" to SBOM list page
- Depends on: Task 4 — Add SBOM comparison page with diff sections
- Depends on: Task 5 — Add MSW mock handlers and test fixtures for comparison endpoint

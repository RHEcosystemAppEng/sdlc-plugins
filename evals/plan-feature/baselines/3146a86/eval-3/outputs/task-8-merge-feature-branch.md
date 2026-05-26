# Task 8 — Merge feature branch TC-9003 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: new SBOM comparison model structs, comparison service logic, comparison endpoint in the backend, frontend API layer, comparison page UI, and SBOM list page selection enhancements.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review for trustify-backend
- [ ] A PR from `TC-9003` to `main` is open and ready for review for trustify-ui
- [ ] PR descriptions summarize all changes made during the feature implementation

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify all tests pass on the feature branch before creating the merge PR

## Dependencies
- Depends on: Task 2 — Add SBOM comparison model structs
- Depends on: Task 3 — Add SBOM comparison service logic
- Depends on: Task 4 — Add SBOM comparison endpoint
- Depends on: Task 5 — Add frontend API layer for SBOM comparison
- Depends on: Task 6 — Add SBOM comparison page with diff sections
- Depends on: Task 7 — Add SBOM selection and "Compare selected" to SbomListPage

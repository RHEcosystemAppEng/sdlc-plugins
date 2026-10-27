## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: database migration from lookup table to enum column, entity definition updates, service/endpoint query simplification, ingestion pipeline update, and integration test updates.

## Acceptance Criteria
- [ ] All intermediate task PRs have been merged into the `TC-9005` feature branch
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] PR description summarizes all changes across the feature

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] All tests pass on the feature branch before opening the merge PR

## Dependencies
- Depends on: Task 2 — Database migration for enum column
- Depends on: Task 3 — Update entity definitions
- Depends on: Task 4 — Update advisory service and endpoints
- Depends on: Task 5 — Update ingestion pipeline
- Depends on: Task 6 — Update integration tests

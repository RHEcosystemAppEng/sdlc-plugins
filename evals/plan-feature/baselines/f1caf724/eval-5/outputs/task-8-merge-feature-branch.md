## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: database migration from advisory status lookup table to PostgreSQL enum column, SeaORM entity updates, service and endpoint query updates, ingestion pipeline updates, integration test updates, and documentation updates. This PR represents the atomic delivery of the advisory status enum conversion — all changes must land together.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes all changes from Tasks 2-7
- [ ] All CI checks pass on the feature branch

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify the combined changes compile and all tests pass on the feature branch
- [ ] Verify the migration runs successfully against a test database

## Dependencies
- Depends on: Task 2 — Create database migration for advisory status enum conversion
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and endpoint queries to use enum status
- Depends on: Task 5 — Update advisory ingestion pipeline for enum status
- Depends on: Task 6 — Update advisory integration tests for enum status
- Depends on: Task 7 — Update documentation for advisory schema change

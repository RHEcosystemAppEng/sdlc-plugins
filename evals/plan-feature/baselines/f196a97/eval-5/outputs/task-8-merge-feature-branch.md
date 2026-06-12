# Task 8 — Merge feature branch TC-9005 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: database migration from advisory_status lookup table to PostgreSQL enum column, updated SeaORM entities, updated advisory service/model/endpoint layers, updated ingestion pipeline, and updated integration tests.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes all changes from Tasks 2-7
- [ ] All CI checks pass on the PR

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2-7) have been merged into the feature branch before creating the merge PR
- [ ] All tests pass on the feature branch before opening the merge PR

## Dependencies
- Depends on: Task 2 — Create migration to replace advisory_status table with enum column
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and models to use enum status column
- Depends on: Task 5 — Update advisory endpoints to use enum status filtering
- Depends on: Task 6 — Update advisory ingestion pipeline to write enum status directly
- Depends on: Task 7 — Update advisory integration tests for enum status column

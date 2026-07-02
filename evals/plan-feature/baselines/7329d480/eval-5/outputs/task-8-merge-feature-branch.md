# Task 8: Merge feature branch TC-9005 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Merge the feature branch `TC-9005` to `main` after all implementation tasks are complete. This delivers the advisory status enum migration, entity updates, service/endpoint changes, ingestion pipeline updates, and integration test updates atomically. The merge ensures that the database schema change and all dependent code changes land together, preventing any intermediate broken state.

## Acceptance Criteria
- [ ] All intermediate task PRs have been merged to the `TC-9005` branch
- [ ] CI passes on the `TC-9005` branch with all changes integrated
- [ ] Feature branch `TC-9005` is merged to `main` via pull request
- [ ] No merge conflicts with `main`
- [ ] Post-merge CI on `main` passes

## Test Requirements
- [ ] Full test suite passes on the merged `main` branch
- [ ] Advisory integration tests confirm enum-based status queries work end-to-end

## Dependencies
- Depends on: Task 2 — Write database migration for advisory status enum
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service, model, and endpoints to use status enum
- Depends on: Task 5 — Update advisory ingestion pipeline for direct enum writes
- Depends on: Task 6 — Update advisory integration tests for status enum

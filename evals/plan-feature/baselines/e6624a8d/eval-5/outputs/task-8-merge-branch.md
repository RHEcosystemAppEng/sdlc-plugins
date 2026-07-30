## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks:
- Database migration creating `advisory_status_enum` type, adding `status` column, backfilling, dropping FK, and dropping `advisory_status` table
- SeaORM entity updates replacing `status_id` FK with `status` enum column
- Advisory service and endpoint updates eliminating `advisory_status` joins
- Ingestion pipeline update writing enum values directly
- Integration test updates reflecting the new schema
- Internal architecture documentation updates

All changes must land together on `main` to maintain database-code consistency.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is created and ready for review
- [ ] PR description summarizes all changes from the feature's implementation tasks
- [ ] All CI checks pass on the feature branch

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify the feature branch builds and all tests pass (`cargo build && cargo test`)
- [ ] Verify the database migration runs successfully on a clean database

## Dependencies
- Depends on: Task 2 — Create database migration for advisory status enum
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and endpoints to use status enum
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum values directly
- Depends on: Task 6 — Update advisory integration tests
- Depends on: Task 7 — Update internal architecture documentation

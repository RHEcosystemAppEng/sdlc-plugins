## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks:

- Database migration creating `advisory_status_enum` type, adding `status` enum column, backfilling data, and dropping the `advisory_status` lookup table
- SeaORM entity definition updates replacing the FK relationship with an enum column
- Advisory service and endpoint query updates eliminating all advisory_status joins
- Ingestion pipeline update to write enum values directly
- Integration test updates verifying the new schema
- Architecture documentation updates reflecting the schema change

All changes must land atomically to avoid leaving the database or application in an inconsistent state.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is created and ready for review
- [ ] The PR description summarizes all changes from the feature's implementation tasks
- [ ] All CI checks pass on the feature branch before the PR is created

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify the full test suite passes on the feature branch (`cargo test`)
- [ ] Verify the migration runs successfully against a clean database

## Dependencies
- Depends on: Task 2 — Create database migration for enum type and column conversion
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and endpoint queries to use enum column
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum values directly
- Depends on: Task 6 — Update advisory integration tests for enum status
- Depends on: Task 7 — Update internal architecture documentation for schema change

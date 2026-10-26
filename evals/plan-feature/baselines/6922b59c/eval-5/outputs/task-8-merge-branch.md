## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks:

- Database migration creating `advisory_status_enum` type, adding `status` column, backfilling data, and dropping the `advisory_status` lookup table
- SeaORM entity updates replacing `status_id` FK with `status` enum column
- Advisory service and endpoint updates to query the enum column directly
- Ingestion pipeline updates to write enum values directly
- Integration test updates for the new schema
- Architecture documentation updates

This PR represents the atomic delivery of the entire TC-9005 feature. All changes were developed on the `TC-9005` feature branch to ensure the coordinated schema migration and code changes land together.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes all changes from Tasks 2 through 7
- [ ] All CI checks pass on the feature branch
- [ ] The PR includes all commits from the intermediate implementation tasks

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify the full test suite passes on the `TC-9005` branch (`cargo test`)
- [ ] Verify the migration runs successfully against a clean database

## Dependencies
- Depends on: Task 2 — Create database migration for advisory status enum
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and endpoints to use enum column
- Depends on: Task 5 — Update advisory ingestion pipeline for enum values
- Depends on: Task 6 — Update advisory integration tests
- Depends on: Task 7 — Update architecture documentation

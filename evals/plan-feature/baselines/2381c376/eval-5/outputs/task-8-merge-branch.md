## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: creation of `advisory_status_enum` PostgreSQL type, migration of `advisory.status_id` FK to `advisory.status` enum column, update of all advisory queries and ingestion pipeline, and removal of the `advisory_status` lookup table. This feature required atomic delivery because database migrations and code changes are interdependent.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] PR description summarizes all changes: enum type creation, status column migration, service/endpoint updates, ingestion pipeline updates, lookup table removal, and documentation updates
- [ ] All CI checks pass on the PR

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch `TC-9005` before creating the merge PR
- [ ] Verify all tests pass on the feature branch (unit tests, integration tests)
- [ ] Verify the full migration sequence runs cleanly: enum creation, backfill, code updates, table drop

## Dependencies
- Depends on: Task 2 -- Database migration to create enum type and add status column
- Depends on: Task 3 -- Update SeaORM entity definitions for new schema
- Depends on: Task 4 -- Update advisory service and endpoints to use enum column
- Depends on: Task 5 -- Update advisory ingestion pipeline
- Depends on: Task 6 -- Database migration to drop status_id and advisory_status table
- Depends on: Task 7 -- Documentation updates

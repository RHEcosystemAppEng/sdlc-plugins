## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks:

- Atomic database migration replacing the `advisory_status` lookup table with a PostgreSQL `advisory_status_enum` column
- Updated SeaORM entity definitions (advisory entity with enum mapping, removed advisory_status entity)
- Updated advisory service layer and endpoints to query the enum column directly (no join)
- Updated advisory ingestion pipeline to write enum values directly
- Updated integration tests for the new schema
- Updated internal architecture documentation

This feature eliminates the `advisory_status` join from all advisory queries, reducing the advisory list endpoint p95 latency by approximately 40ms and simplifying the schema.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] PR description summarizes all changes across all feature tasks
- [ ] All CI checks pass on the PR

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch `TC-9005` before creating the merge PR
- [ ] Verify all tests pass on the feature branch before opening the PR
- [ ] Verify the migration runs successfully against a clean database

## Dependencies
- Depends on: Task 2 -- Create atomic database migration
- Depends on: Task 3 -- Update SeaORM entity definitions
- Depends on: Task 4 -- Update advisory service layer and endpoints
- Depends on: Task 5 -- Update advisory ingestion pipeline
- Depends on: Task 6 -- Update integration tests
- Depends on: Task 7 -- Update internal architecture documentation

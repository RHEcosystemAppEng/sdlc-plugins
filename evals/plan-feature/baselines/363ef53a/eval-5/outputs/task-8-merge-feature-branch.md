## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks:

- Database migration from `advisory_status` lookup table to `advisory_status_enum` PostgreSQL enum column
- Updated SeaORM entity definitions with `DeriveActiveEnum` enum mapping
- Updated advisory service, endpoints, and search queries to use direct enum column
- Updated advisory ingestion pipeline for direct enum writes
- Updated integration tests for the new schema
- Updated internal architecture documentation

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] PR description summarizes all changes across the feature's tasks
- [ ] All CI checks pass on the feature branch

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] All tests pass on the feature branch (`cargo test`)
- [ ] Migration runs successfully against a clean test database

## Dependencies
- Depends on: Task 2 -- Create database migration for advisory status enum conversion
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 -- Update advisory service and endpoints to use status enum
- Depends on: Task 5 -- Update advisory ingestion pipeline for direct enum writes
- Depends on: Task 6 -- Update advisory integration tests for status enum

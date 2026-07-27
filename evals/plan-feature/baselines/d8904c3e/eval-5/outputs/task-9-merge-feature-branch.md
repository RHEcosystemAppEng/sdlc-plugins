## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks:

- Database migration replacing `advisory_status` lookup table with `advisory_status_enum` PostgreSQL enum column
- Updated SeaORM entity definitions for the advisory entity
- Updated advisory service, model, and endpoint layers to use enum column directly
- Updated advisory ingestion pipeline for direct enum value writes
- Updated integration tests for the new schema
- Updated internal architecture documentation

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] PR description summarizes all changes made in the feature branch
- [ ] All CI checks pass on the PR

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] All tests pass on the feature branch (`cargo test`)

## Dependencies
- Depends on: Task 2 — Database migration
- Depends on: Task 3 — Update SeaORM entity definitions
- Depends on: Task 4 — Update advisory service and model layer
- Depends on: Task 5 — Update advisory endpoints
- Depends on: Task 6 — Update advisory ingestion pipeline
- Depends on: Task 7 — Update integration tests
- Depends on: Task 8 — Documentation updates

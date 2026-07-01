## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: database migration from `advisory_status` lookup table to `advisory_status_enum` PostgreSQL enum column, SeaORM entity updates, advisory service/model/endpoint updates, ingestion pipeline updates, and integration test updates.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] PR description summarizes all changes: migration, entity updates, service/model refactor, endpoint updates, ingestion pipeline changes, and test updates

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] `cargo test` passes on the feature branch with all changes integrated
- [ ] Migration up/down works correctly with the complete changeset

## Dependencies
- Depends on: Task 2 — Create enum migration
- Depends on: Task 3 — Update SeaORM entity definitions
- Depends on: Task 4 — Update advisory service and models
- Depends on: Task 5 — Update advisory endpoints
- Depends on: Task 6 — Update ingestion pipeline
- Depends on: Task 7 — Update integration tests

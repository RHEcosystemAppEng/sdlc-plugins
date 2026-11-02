## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks:
- Database migration: replaced `advisory_status` lookup table with `advisory_status_enum` PostgreSQL enum column
- Entity updates: updated SeaORM advisory entity to use enum type
- Service/endpoint updates: removed advisory_status joins from all advisory queries
- Ingestion pipeline: writes enum values directly
- Integration tests: updated to validate enum-based status

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] PR description summarizes all changes from Tasks 2-7
- [ ] All CI checks pass on the PR

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify the feature branch is up to date with `main` (rebased or merged)

## Dependencies
- Depends on: Task 2 — Database migration
- Depends on: Task 3 — Update entity definitions
- Depends on: Task 4 — Update advisory service and endpoints
- Depends on: Task 5 — Update ingestion pipeline
- Depends on: Task 6 — Update integration tests

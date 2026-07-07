# Task 8 — Merge feature branch TC-9005 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks:

- Database migration replacing the `advisory_status` lookup table with `advisory_status_enum` PostgreSQL enum column
- SeaORM entity definition updates (new `AdvisoryStatusEnum` type, removed `advisory_status` entity)
- Advisory service and endpoint updates to query the enum column directly
- Ingestion pipeline updates to write enum values directly
- Integration test updates for the new schema
- Internal architecture documentation updates

This PR delivers the complete advisory status enum migration as an atomic unit, ensuring that the database schema change and all dependent code changes land on `main` together.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes all changes from Tasks 2-7
- [ ] All CI checks pass on the feature branch

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify the feature branch is up to date with `main` (rebased or merged)
- [ ] Verify all tests pass on the feature branch (`cargo test`)

## Dependencies
- Depends on: Task 2 — Create database migration for advisory status enum
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and endpoints to use status enum column
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum values directly
- Depends on: Task 6 — Update advisory integration tests for status enum migration
- Depends on: Task 7 — Update internal architecture documentation for advisory status enum migration

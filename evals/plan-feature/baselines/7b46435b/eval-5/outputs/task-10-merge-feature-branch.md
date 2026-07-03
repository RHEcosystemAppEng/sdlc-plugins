# Task 10 — Merge feature branch TC-9005 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: database migration from the `advisory_status` lookup table to an `advisory_status_enum` PostgreSQL enum column, SeaORM entity definition updates, advisory model and service layer changes to eliminate the status table join, endpoint updates for direct enum filtering, ingestion pipeline updates for direct enum writes, and integration test updates.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify the full test suite passes on the feature branch: `cargo test --all`

## Dependencies
- Depends on: Task 2 — Create database migration for advisory status enum conversion
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory model structs for direct enum status
- Depends on: Task 5 — Update advisory service to eliminate status table join
- Depends on: Task 6 — Update advisory endpoints for enum status filtering
- Depends on: Task 7 — Update advisory ingestion pipeline for direct enum writes
- Depends on: Task 8 — Update advisory integration tests for new schema
- Depends on: Task 9 — Update documentation for advisory schema change

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: database migration from `advisory_status` lookup table to `advisory_status_enum` PostgreSQL enum column, entity definition updates, service/model layer changes, endpoint updates, ingestion pipeline changes, integration test updates, and documentation updates.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes all changes from Tasks 2-8
- [ ] All CI checks pass on the PR

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify the full test suite passes on the feature branch: `cargo test`
- [ ] Verify the database migration applies cleanly from a fresh `main` state

## Dependencies
- Depends on: Task 2 — Add database migration for advisory status enum conversion
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and model layer to use enum status
- Depends on: Task 5 — Update advisory REST endpoints for enum status filtering
- Depends on: Task 6 — Update advisory ingestion pipeline for direct enum writes
- Depends on: Task 7 — Update advisory integration tests for enum status

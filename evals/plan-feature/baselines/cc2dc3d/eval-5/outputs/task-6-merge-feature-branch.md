# Task 6 — Merge feature branch TC-9005 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: database migration from `advisory_status` lookup table to `advisory_status_enum` column, entity definition updates, service/endpoint/ingestion pipeline updates, and integration test updates. All intermediate task PRs must be merged into the feature branch before creating this merge PR.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes all changes from Tasks 2-5
- [ ] All CI checks pass on the merge PR

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2-5) have been merged into the feature branch before creating the merge PR
- [ ] Verify the full test suite passes on the feature branch: `cargo test`
- [ ] Verify the migration runs cleanly on a fresh database

## Dependencies
- Depends on: Task 2 — Create migration to add advisory_status_enum and migrate data
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service, endpoints, and ingestion pipeline to use enum status
- Depends on: Task 5 — Update advisory integration tests for enum status schema

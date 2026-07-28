## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: the atomic database migration from the `advisory_status` lookup table to the `advisory_status_enum` column, SeaORM entity updates, advisory service and model layer changes, ingestion pipeline updates, integration test updates, and documentation updates. This PR represents the coordinated delivery of all feature components that must land atomically.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] PR description summarizes all changes from Tasks 2-7
- [ ] All CI checks pass on the feature branch

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Full test suite passes on the feature branch (`cargo test`)
- [ ] Migration runs successfully against a clean database

## Dependencies
- Depends on: Task 2 — Create database migration for advisory status enum
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and model to use enum column
- Depends on: Task 5 — Update advisory ingestion pipeline for enum status
- Depends on: Task 6 — Update advisory integration tests
- Depends on: Task 7 — Update internal architecture documentation

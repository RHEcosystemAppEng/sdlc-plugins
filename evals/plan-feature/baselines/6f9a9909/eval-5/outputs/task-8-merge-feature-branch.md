# Task 8 — Merge feature branch TC-9005 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks:

- Database migration creating `advisory_status_enum` PostgreSQL type and converting `advisory.status_id` FK to `advisory.status` enum column
- SeaORM entity definitions updated to use `DeriveActiveEnum` for the status field
- Advisory service and endpoint queries simplified by removing the `advisory_status` join
- Ingestion pipeline updated to write enum values directly
- Integration tests updated to verify enum-based advisory operations
- Internal architecture documentation updated to reflect the new schema

This PR represents the coordinated delivery of all changes required to drop the `advisory_status` lookup table and migrate to an enum column, as required by the feature's atomicity constraints.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] PR description summarizes all changes made across the feature's tasks
- [ ] All CI checks pass on the PR
- [ ] All intermediate task PRs have been merged into the `TC-9005` feature branch

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify the feature branch is up to date with `main` (rebase or merge `main` into the feature branch if needed)
- [ ] Verify all integration tests pass on the feature branch

## Dependencies
- Depends on: Task 2 — Create database migration for advisory status enum conversion
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status
- Depends on: Task 4 — Update advisory service and endpoints for enum status
- Depends on: Task 5 — Update advisory ingestion pipeline for enum status
- Depends on: Task 6 — Update advisory integration tests for enum status
- Depends on: Task 7 — Update internal architecture documentation

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: creation of the `advisory_status_enum` PostgreSQL enum type, migration from the `advisory_status` lookup table to an enum column on the `advisory` table, updates to SeaORM entity definitions, advisory service and endpoint query updates, ingestion pipeline changes, integration test updates, and documentation updates. This PR represents the atomic delivery of the entire feature — all changes land together to maintain database-code consistency.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes all changes from the feature's implementation tasks
- [ ] All CI checks pass on the PR

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch `TC-9005` before creating the merge PR
- [ ] Verify the full test suite passes on the feature branch before opening the PR

## Dependencies
- Depends on: Task 2 — Create database migration for advisory_status_enum
- Depends on: Task 3 — Update SeaORM entity definitions
- Depends on: Task 4 — Update advisory service and endpoint queries
- Depends on: Task 5 — Update advisory ingestion pipeline
- Depends on: Task 6 — Update advisory integration tests
- Depends on: Task 7 — Update internal architecture documentation

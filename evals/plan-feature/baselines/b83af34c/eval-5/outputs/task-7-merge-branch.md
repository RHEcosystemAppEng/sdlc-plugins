## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Merge feature branch TC-9005 to main, delivering the complete advisory status enum migration atomically. This PR aggregates all intermediate changes: the database migration, entity definition updates, advisory service and endpoint changes, and ingestion pipeline updates. The atomic merge ensures no partial state reaches main — the migration and all dependent code changes land together.

## Acceptance Criteria
- [ ] All intermediate tasks (Tasks 2-5) are completed and merged to the feature branch
- [ ] PR from TC-9005 to main is created and passes CI
- [ ] All advisory endpoint integration tests pass against the merged changes
- [ ] No references to the `advisory_status` lookup table remain in the codebase
- [ ] The advisory list endpoint demonstrates reduced latency without the status join

## Test Requirements
- [ ] Full CI suite passes on the merge PR
- [ ] Advisory endpoint integration tests verify correct status handling with the enum column
- [ ] Migration runs successfully against a clean database and a database with existing data

## Dependencies
- Depends on: Task 2 — Create database migration for advisory status enum
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service, model, and endpoints to use enum column
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum values directly

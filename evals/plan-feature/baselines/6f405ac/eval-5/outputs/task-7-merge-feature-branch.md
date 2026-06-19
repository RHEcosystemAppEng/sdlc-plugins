# Task 7 — Merge feature branch TC-9005 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create PR to merge TC-9005 into main. All intermediate tasks (database migration, entity updates, service/endpoint updates, ingestion pipeline updates, and integration test updates) must be merged into the feature branch before this PR is opened.

## Acceptance Criteria
- [ ] PR from TC-9005 to main is open

## Test Requirements
- [ ] Verify all intermediate PRs merged into feature branch

## Dependencies
- Depends on: Task 2 — Create database migration to replace advisory_status table with enum column
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and endpoints to use enum column
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum values directly
- Depends on: Task 6 — Update advisory integration tests for enum status column

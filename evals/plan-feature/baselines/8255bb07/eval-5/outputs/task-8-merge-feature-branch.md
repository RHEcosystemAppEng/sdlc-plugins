## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: database migration from `advisory_status` lookup table to `advisory_status_enum` column, SeaORM entity definition updates, advisory service and endpoint query simplification, ingestion pipeline updates, integration test updates, and architecture documentation updates.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes all changes from the feature's implementation tasks

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify the feature branch builds and all tests pass before opening the PR

## Dependencies
- Depends on: Task 2 -- Create database migration for advisory status enum conversion
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 -- Update advisory service, models, and endpoints to use status enum
- Depends on: Task 5 -- Update advisory ingestion pipeline for status enum
- Depends on: Task 6 -- Update advisory integration tests for status enum
- Depends on: Task 7 -- Update internal architecture documentation

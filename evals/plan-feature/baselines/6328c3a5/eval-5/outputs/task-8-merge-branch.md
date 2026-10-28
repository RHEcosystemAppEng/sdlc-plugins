## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks:
- Database migration creating the `advisory_status_enum` type and converting the `advisory` table
- SeaORM entity updates replacing the FK-based status with an enum column
- Advisory service and endpoint updates eliminating the lookup table join
- Advisory ingestion pipeline updates for direct enum writes
- Updated integration tests validating the new enum-based queries

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] PR description summarizes all changes from the feature's implementation tasks
- [ ] All CI checks pass on the PR

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify the feature branch builds successfully with all changes combined
- [ ] Verify all integration tests pass on the combined feature branch

## Dependencies
- Depends on: Task 2 -- Create database migration for advisory status enum conversion
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 -- Update advisory service and endpoints to use status enum column
- Depends on: Task 5 -- Update advisory ingestion pipeline for direct enum writes
- Depends on: Task 6 -- Update advisory integration tests for status enum

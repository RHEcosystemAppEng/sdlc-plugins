## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks:

- Database migration replacing `advisory_status` lookup table with `advisory_status_enum` PostgreSQL enum column
- SeaORM entity updates reflecting the new enum-based schema
- Advisory service and endpoint updates eliminating lookup table joins
- Ingestion pipeline updates to write enum values directly
- Integration test updates for the new schema
- Internal architecture documentation updates

This PR delivers the complete feature atomically -- all schema, code, test, and documentation changes land together to prevent any intermediate broken state on `main`.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] PR description summarizes all changes from the feature's tasks
- [ ] All CI checks pass on the feature branch

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] All integration tests pass on the feature branch with the combined changes
- [ ] Migration applies and rolls back cleanly on the feature branch

## Dependencies
- Depends on: Task 2 -- Create database migration for advisory status enum
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 -- Update advisory service and endpoints to use status enum
- Depends on: Task 5 -- Update advisory ingestion pipeline to write enum values
- Depends on: Task 6 -- Update advisory integration tests for status enum
- Depends on: Task 7 -- Update internal architecture documentation

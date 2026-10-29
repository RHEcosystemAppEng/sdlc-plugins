## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks:

- Database migration converting `advisory_status` lookup table to `advisory_status_enum` PostgreSQL enum column
- Updated SeaORM entity definitions with `AdvisoryStatusEnum` derive macro
- Advisory service and endpoint queries updated to use enum column directly (eliminating join overhead)
- Advisory ingestion pipeline updated to write enum values directly
- Internal architecture documentation updated to reflect schema change

This PR represents the atomic delivery of all advisory status enum migration changes, ensuring that `main` never has a partially applied migration.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] PR description summarizes all changes from Tasks 2-6
- [ ] All CI checks pass on the feature branch before the merge PR is created

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2-6) have been merged into the feature branch `TC-9005` before creating the merge PR
- [ ] Verify the feature branch builds and all tests pass (`cargo test`)
- [ ] Verify the database migration runs successfully on a clean database

## Dependencies
- Depends on: Task 2 -- Create database migration for advisory status enum conversion
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 -- Update advisory service layer and endpoints to use enum status
- Depends on: Task 5 -- Update advisory ingestion pipeline to write enum values directly
- Depends on: Task 6 -- Update internal architecture documentation

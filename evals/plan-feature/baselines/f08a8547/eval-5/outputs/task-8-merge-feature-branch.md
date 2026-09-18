## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks:

- Database migration creating `advisory_status_enum` type, adding `status` column with backfill, dropping `status_id` FK and `advisory_status` lookup table
- SeaORM entity updates defining `AdvisoryStatusEnum` and replacing `status_id` with `status` column
- Advisory service and endpoint changes eliminating the lookup table join for direct enum column access
- Ingestion pipeline updates writing enum values directly instead of through the lookup table
- Integration test updates for the new enum-based schema
- Internal architecture documentation updates

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] All intermediate task PRs have been merged into the `TC-9005` feature branch
- [ ] The PR description summarizes all changes across the feature

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify the full test suite passes on the feature branch (`cargo test`)
- [ ] Verify no merge conflicts exist between `TC-9005` and `main`

## Dependencies
- Depends on: Task 2 -- Create database migration for advisory status enum
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 -- Update advisory service and endpoints to use enum column
- Depends on: Task 5 -- Update advisory ingestion pipeline to write enum values directly
- Depends on: Task 6 -- Update advisory integration tests

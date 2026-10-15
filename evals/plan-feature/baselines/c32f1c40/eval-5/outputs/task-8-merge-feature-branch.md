## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks:

- Database migration: created `advisory_status_enum` PostgreSQL enum type, added `status` enum column to `advisory` table with backfill, dropped `status_id` FK column and `advisory_status` lookup table
- Entity updates: updated SeaORM `advisory` entity to use enum field, removed `advisory_status` entity
- Service/endpoint updates: removed all `advisory_status` joins from advisory queries, updated filtering to use enum column directly
- Ingestion updates: pipeline writes enum values directly instead of lookup table entries
- Test updates: integration tests use new enum schema
- Documentation: internal architecture docs updated to reflect schema change

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] All intermediate task PRs have been merged into the feature branch
- [ ] The PR description summarizes all changes across all tasks
- [ ] CI passes on the feature branch

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify CI/tests pass on the feature branch with all changes combined

## Dependencies
- Depends on: Task 2 -- Create advisory status enum migration
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 -- Update advisory service and endpoints to use status enum
- Depends on: Task 5 -- Update advisory ingestion pipeline for status enum
- Depends on: Task 6 -- Update advisory integration tests

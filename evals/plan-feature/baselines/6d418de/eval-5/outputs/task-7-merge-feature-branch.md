# Task 7 — Merge feature branch TC-9005 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks:

- Database migration replacing `advisory_status` lookup table with `advisory_status_enum` PostgreSQL enum column on the `advisory` table
- SeaORM entity definitions updated to use `AdvisoryStatusEnum` enum type
- Advisory service and endpoints updated to query enum column directly (eliminating join)
- Ingestion pipeline updated to write enum values directly
- Integration tests updated for new schema

This PR delivers the complete advisory status enum migration as an atomic change, ensuring no partial state reaches `main`.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] All intermediate task PRs have been merged into the feature branch
- [ ] CI passes on the merge PR
- [ ] PR description summarizes all changes from Tasks 2-6

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2-6) have been merged into the feature branch before creating the merge PR
- [ ] All tests pass on the feature branch

## Dependencies
- Depends on: Task 2 — Create migration to replace advisory_status table with enum column
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and endpoints to use enum column
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum values directly
- Depends on: Task 6 — Update integration tests for advisory status enum migration

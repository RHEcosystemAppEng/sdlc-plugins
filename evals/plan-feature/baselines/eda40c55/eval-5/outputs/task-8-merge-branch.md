## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks:
- Database migration converting `advisory_status` lookup table to `advisory_status_enum` PostgreSQL enum column
- SeaORM entity updates replacing `status_id` foreign key with `status` enum column
- Advisory service and endpoint updates eliminating the status join from all queries
- Ingestion pipeline updates writing enum values directly
- Integration test updates for the new schema
- Internal architecture documentation updates

All changes must land together to maintain database-code consistency. The migration, entity definitions, service layer, ingestion pipeline, and tests are tightly coupled — partial delivery would leave the codebase in an inconsistent state.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] PR description summarizes all changes across the feature's tasks
- [ ] All CI checks pass on the feature branch
- [ ] All intermediate task PRs have been merged into the feature branch

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify the feature branch is up to date with `main` (no merge conflicts)
- [ ] Verify CI pipeline passes on the complete feature branch

## Dependencies
- Depends on: Task 2 — Create migration for advisory status enum conversion
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service layer and endpoints to use status enum
- Depends on: Task 5 — Update advisory ingestion pipeline for status enum
- Depends on: Task 6 — Update advisory integration tests for status enum
- Depends on: Task 7 — Update internal architecture documentation

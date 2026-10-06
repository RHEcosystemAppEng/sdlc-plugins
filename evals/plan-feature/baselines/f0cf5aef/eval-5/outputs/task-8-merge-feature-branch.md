## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: database migration from `advisory_status` lookup table to `advisory_status_enum` PostgreSQL enum column, SeaORM entity updates, advisory service and endpoint updates, ingestion pipeline updates, integration test updates, and documentation updates. This PR delivers the complete advisory status enum migration atomically to main.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] PR description summarizes all changes from Tasks 2-7
- [ ] All CI checks pass on the feature branch

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2-7) have been merged into the `TC-9005` feature branch before creating the merge PR
- [ ] Verify the feature branch is up to date with `main` (rebase or merge main into feature branch if needed)
- [ ] Verify all tests pass on the feature branch: `cargo test --all`

## Dependencies
- Depends on: Task 2 — Create database migration for advisory status enum conversion
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and endpoints to use status enum column
- Depends on: Task 5 — Update advisory ingestion pipeline for direct enum writes
- Depends on: Task 6 — Update integration tests for advisory status enum
- Depends on: Task 7 — Update internal architecture documentation

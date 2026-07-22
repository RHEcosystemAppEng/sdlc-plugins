## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: the atomic database migration from the `advisory_status` lookup table to an `advisory_status_enum` PostgreSQL enum column, updated SeaORM entity definitions, updated advisory service/model/endpoint layers, updated ingestion pipeline, and updated integration tests. All intermediate task PRs must be merged into the feature branch before creating this merge PR.

## Acceptance Criteria
- [ ] All intermediate task PRs have been merged into the `TC-9005` feature branch
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes all changes from the feature's tasks
- [ ] CI passes on the merge PR

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify the full test suite passes on the feature branch (`cargo test`)
- [ ] Verify the migration runs successfully against a test database from the merged feature branch

## Dependencies
- Depends on: Task 2 — Add database migration for advisory status enum conversion
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status
- Depends on: Task 4 — Update advisory service, model, and endpoint layers
- Depends on: Task 5 — Update advisory ingestion pipeline
- Depends on: Task 6 — Update advisory integration tests
- Depends on: Task 7 — Update internal architecture documentation

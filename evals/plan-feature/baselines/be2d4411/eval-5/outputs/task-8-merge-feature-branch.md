## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: database migration from `advisory_status` lookup table to `advisory_status_enum` PostgreSQL enum column, SeaORM entity updates, advisory service/model query simplification, endpoint filter updates, ingestion pipeline refactor, and integration test updates. This PR represents the atomic delivery of the entire advisory status enum migration feature.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] PR description summarizes all changes: migration, entity updates, service changes, endpoint updates, ingestion refactor, test updates
- [ ] All CI checks pass on the PR
- [ ] No merge conflicts with `main`

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch `TC-9005` before creating the merge PR
- [ ] Verify all tests pass on the feature branch (`cargo test --workspace`)
- [ ] Verify the migration runs successfully against a clean database

## Dependencies
- Depends on: Task 2 — Create database migration for advisory status enum
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and model to use status enum column
- Depends on: Task 5 — Update advisory endpoints to query status enum directly
- Depends on: Task 6 — Update advisory ingestion pipeline for enum status values
- Depends on: Task 7 — Update integration tests for advisory status enum migration

## Labels
- ai-generated-jira

## additional_fields
- priority: High
- fixVersions: RHTPA 2.0.0

[sdlc-workflow] Description digest: sha256-md:2f7d062dfc38acca0f36a2c367c81ec3c9e229aa334d75c13b0c6736fc77a4b2

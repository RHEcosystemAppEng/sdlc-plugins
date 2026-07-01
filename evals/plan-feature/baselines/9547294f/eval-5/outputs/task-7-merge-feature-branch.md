# Task 7 — Merge feature branch TC-9005 to main

**Priority:** High
**Fix Versions:** RHTPA 2.0.0
**Labels:** ai-generated-jira

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: PostgreSQL enum type creation, advisory status column migration, SeaORM entity updates, service layer query simplification, ingestion pipeline update, and endpoint/test updates. All intermediate task PRs must be merged into the feature branch before creating this merge PR.

## Acceptance Criteria
- [ ] All intermediate task PRs (Tasks 2-6) have been merged into the `TC-9005` feature branch
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes all changes: enum migration, entity updates, service layer changes, ingestion pipeline update, endpoint and test updates
- [ ] All tests pass on the feature branch

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify the full test suite passes on the feature branch (`cargo test`)
- [ ] Verify the migration runs successfully against a clean database

## Dependencies
- Depends on: Task 2 — Create migration to add advisory_status_enum and migrate status column
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and model to use enum status column
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum status directly
- Depends on: Task 6 — Update advisory endpoints and integration tests

[sdlc-workflow] Description digest: sha256-md:a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8

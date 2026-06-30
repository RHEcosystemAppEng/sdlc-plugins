# Task 7 — Merge feature branch TC-9005 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: database migration from advisory_status lookup table to advisory_status_enum column, entity definition updates, service/endpoint query simplification, ingestion pipeline updates, and integration test updates. This ensures all changes land atomically on main, preventing any inconsistent state between the schema and application code.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes all changes from Tasks 2-6
- [ ] All CI checks pass on the PR

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2-6) have been merged into the feature branch before creating the merge PR
- [ ] Verify that the full test suite passes on the feature branch before opening the PR

## Dependencies
- Depends on: Task 2 — Create database migration for advisory status enum
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and endpoints to use status enum
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum values directly
- Depends on: Task 6 — Update advisory integration tests for status enum

[sdlc-workflow] Description digest: sha256-md:324835cd3ffcccbec99e0b1bc5c2c1196f32ab7daa335be04a5ebd3ea6678058

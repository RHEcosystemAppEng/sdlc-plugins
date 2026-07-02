# Task 7 — Merge feature branch TC-9005 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: database migration from advisory status lookup table to PostgreSQL enum column, SeaORM entity updates, advisory service/model layer changes, ingestion pipeline updates, and integration test updates. This ensures all advisory status enum changes land atomically on `main`.

## Acceptance Criteria
- [ ] All intermediate task PRs (Tasks 2-6) have been merged into the `TC-9005` feature branch
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes all changes: migration, entity updates, service layer, ingestion pipeline, and tests
- [ ] All CI checks pass on the merge PR
- [ ] No merge conflicts with `main`

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify the full test suite passes on the feature branch: `cargo test`
- [ ] Verify the migration runs successfully against a clean database
- [ ] Verify no regressions in advisory endpoint behavior

## Dependencies
- Depends on: Task 2 — Create database migration for advisory status enum conversion
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and model layer to use status enum column
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum values directly
- Depends on: Task 6 — Update advisory integration tests for status enum

---

[sdlc-workflow] Description digest: sha256-md:3d200f52525f4ab452fd31073e8f5f2072452acf232a0ce58517a04ccacf154a

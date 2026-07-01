# Task 7 — Merge feature branch TC-9005 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: migration from advisory status lookup table to PostgreSQL enum column, entity definition updates, service layer query simplification, ingestion pipeline update, and endpoint/test updates.

## Acceptance Criteria
- [ ] All intermediate task PRs have been merged into the feature branch `TC-9005`
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] All CI checks pass on the merge PR
- [ ] The PR description summarizes the complete set of changes from all intermediate tasks

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Full test suite passes on the feature branch with all changes integrated
- [ ] Migration runs successfully against a clean database

## Dependencies
- Depends on: Task 2 — Create migration to add advisory status enum and drop lookup table
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and model to use enum column
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum values directly
- Depends on: Task 6 — Update advisory endpoints and integration tests

---
Description Digest: sha256-md:0e6ce2c67a0a65208c8a9df4736e42d41feca8ca8cdf61c8cee71754ba5f8ec0
Priority: High
Fix Versions: RHTPA 2.0.0

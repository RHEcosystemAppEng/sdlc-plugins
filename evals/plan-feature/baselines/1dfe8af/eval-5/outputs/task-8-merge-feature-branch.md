# Task 8 — Merge feature branch TC-9005 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a pull request to merge feature branch TC-9005 into main. This PR represents the complete, atomic delivery of the advisory status enum migration: the database migration, entity updates, service/endpoint changes, ingestion pipeline updates, and test modifications all land on main together. This ensures there is no window where the schema and code are out of sync.

## Acceptance Criteria
- [ ] PR from TC-9005 to main is open and ready for review
- [ ] All intermediate task PRs have been merged into the TC-9005 feature branch
- [ ] CI passes on the TC-9005 branch (all tests green)
- [ ] PR description summarizes the complete set of changes

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2-7) are merged into the TC-9005 feature branch
- [ ] Verify CI pipeline passes on the feature branch before opening the PR
- [ ] Verify no merge conflicts with main

## Dependencies
- Depends on: Task 2 — Create atomic migration: enum type, backfill, and table drop
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service layer and models to use enum column
- Depends on: Task 5 — Update advisory endpoints for enum-based status filtering
- Depends on: Task 6 — Update advisory ingestion pipeline to write enum values directly
- Depends on: Task 7 — Update integration tests for advisory status enum

[sdlc-workflow] Description digest: sha256-md:b3d7e0f89c2a4615d8f1b6c97a0e5d48f9c2b1a67d3e8f0526c4a7b9e1d3f6a5

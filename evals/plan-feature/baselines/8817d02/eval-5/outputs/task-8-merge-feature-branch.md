# Task 8 — Merge feature branch TC-9005 to main

## Summary

Merge feature branch TC-9005 to main

## Repository

trustify-backend

## Target Branch

main

## Bookend Type

merge-branch

## Description

Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: database migration from advisory_status lookup table to enum column, entity definition updates, service and model updates, ingestion pipeline changes, endpoint updates, and integration test updates.

## Acceptance Criteria

- [ ] All intermediate task PRs have been merged into the `TC-9005` feature branch
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] All CI checks pass on the merge PR
- [ ] The PR description summarizes all changes from Tasks 2 through 7

## Test Requirements

- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify CI passes on the merge PR (all tests, linting, and build checks)

## Dependencies

- Depends on: Task 2 — Add database migration for advisory status enum column
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and models to use enum status
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum values directly
- Depends on: Task 6 — Update advisory endpoints for enum-based status filtering
- Depends on: Task 7 — Update advisory integration tests for enum status

sha256-md:619cb9d2858c352295cc6c9d16ce272c52fe899062925982709b3f8e617e71f3

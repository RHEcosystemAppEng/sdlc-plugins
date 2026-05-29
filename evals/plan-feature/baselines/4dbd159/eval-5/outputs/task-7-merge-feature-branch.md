# Task 7 — Merge feature branch TC-9005 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks:
- Atomic database migration replacing the `advisory_status` lookup table with an `advisory_status_enum` PostgreSQL enum column on the `advisory` table
- Updated SeaORM entity definitions (new enum type, removed advisory_status entity)
- Updated advisory service, models, and endpoints to query the enum column directly (no join)
- Updated ingestion pipeline to write enum values directly
- Updated integration tests for the new schema

This migration eliminates the `advisory_status` join from all advisory queries, reducing advisory list endpoint p95 latency by ~40ms and simplifying the data model.

## Acceptance Criteria
- [ ] All intermediate task PRs (Tasks 2-6) have been merged into the feature branch `TC-9005`
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes all changes across the feature
- [ ] All CI checks pass on the merge PR

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Full test suite (`cargo test`) passes on the feature branch tip
- [ ] Migration runs successfully against a clean database and against a database with existing data

## Dependencies
- Depends on: Task 2 — Create atomic migration to replace advisory_status table with enum column
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and endpoints to use enum column
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum values directly
- Depends on: Task 6 — Update advisory integration tests for enum-based status

# Task 7 — Merge feature branch TC-9005 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks:
- Task 2: atomic, reversible migration creating `advisory_status_enum`, adding and backfilling `advisory.status`, dropping `advisory.status_id` and the `advisory_status` table
- Task 3: SeaORM `advisory` entity uses the `AdvisoryStatus` enum; `advisory_status` entity removed
- Task 4: advisory service, models, list endpoint filter, and search service use `advisory.status` with no join; API response shape unchanged
- Task 5: advisory ingestion writes enum values directly and rejects unknown statuses
- Task 6: internal architecture docs updated

The PR description must call out that the migration has to be validated against a production-sized dataset before deployment, and that the migration and code are deployed together.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes the changes from Tasks 2–6 and links feature TC-9005

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2, 3, 4, 5, 6) have been merged into the `TC-9005` feature branch before creating the merge PR
- [ ] Verify CI (build, migration tests, integration tests) passes on the `TC-9005` branch head

## Dependencies
- Depends on: Task 2 — Add migration converting advisory_status lookup table to advisory_status_enum column
- Depends on: Task 3 — Update SeaORM advisory entity to use AdvisoryStatus enum column
- Depends on: Task 4 — Replace advisory_status joins with advisory.status column in advisory and search queries
- Depends on: Task 5 — Write advisory status enum directly in advisory ingestion pipeline
- Depends on: Task 6 — Update internal architecture documentation for advisory status enum migration

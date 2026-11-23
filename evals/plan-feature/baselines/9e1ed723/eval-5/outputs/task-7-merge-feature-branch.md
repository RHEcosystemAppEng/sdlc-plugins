**Summary:** Merge feature branch TC-9005 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks:
- Task 2: reversible, atomic migration `m0002_advisory_status_enum`. It creates `advisory_status_enum`, adds and backfills `advisory.status`, and drops `advisory.status_id` and the `advisory_status` table
- Task 3: SeaORM `Advisory` entity uses the `AdvisoryStatus` active enum, and the lookup entity is removed
- Task 4: advisory service, models, endpoints and search queries read and filter `advisory.status` without the join. The API response shape is unchanged
- Task 5: the ingestion pipeline maps feed status to the enum and writes it directly, and rejects unknown statuses
- Task 6: internal architecture documentation updated

This is the single merge that lands the coordinated schema and code change on `main`, as required by the Feature's "all changes must land together" NFR.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes the changes from Tasks 2–6 and links TC-9005

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2, 3, 4, 5, 6) have been merged into the feature branch `TC-9005` before creating the merge PR
- [ ] Verify CI on the `TC-9005` → `main` PR is green (full build, migration tests and API integration tests)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Add reversible migration replacing advisory_status table with advisory_status_enum column
- Depends on: Task 3 — Update SeaORM Advisory entity to use status enum column
- Depends on: Task 4 — Remove advisory_status join from advisory and search queries
- Depends on: Task 5 — Write advisory status enum directly in ingestion pipeline
- Depends on: Task 6 — Update internal architecture docs for advisory status enum

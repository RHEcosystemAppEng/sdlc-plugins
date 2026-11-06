**Summary:** Merge feature branch TC-9005 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks:

- Task 2: reversible, atomic migration `m0002_advisory_status_enum`. It creates `advisory_status_enum`, adds and backfills `advisory.status`, and drops `advisory.status_id` and the `advisory_status` table. The backfill fails closed.
- Task 3: SeaORM `advisory` entity now uses the `AdvisoryStatus` active enum. The `advisory_status` entity is removed.
- Task 4: all advisory queries (service, list/get endpoints, models, search) read `advisory.status` directly with no join. The API response shape is unchanged, and an invalid status filter returns 400.
- Task 5: the ingestion pipeline writes `AdvisoryStatus` directly and rejects unknown statuses.
- Task 6: internal architecture docs updated.

The PR description must also state that the migration and the code changes must be deployed together, and include the production-sized dataset migration timing from Task 2.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes the changes from Tasks 2–6 and the deployment note (deploy migration and code together)

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2, 3, 4, 5, 6) have been merged into the `TC-9005` feature branch before creating the merge PR
- [ ] Verify CI on the `TC-9005` → `main` PR is green (full workspace build, migration tests, advisory, search and ingestion tests)

## Dependencies
- Depends on: Task 2 — Add reversible migration converting advisory_status lookup table to advisory_status_enum column
- Depends on: Task 3 — Update SeaORM advisory entity to use AdvisoryStatus enum column and remove advisory_status entity
- Depends on: Task 4 — Replace advisory_status joins with the advisory.status enum column in all advisory queries
- Depends on: Task 5 — Update advisory ingestion pipeline to write AdvisoryStatus enum values directly
- Depends on: Task 6 — Update internal architecture docs for advisory status enum column

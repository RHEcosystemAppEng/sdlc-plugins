## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks:

- Atomic, reversible migration creating `advisory_status_enum`, adding and backfilling `advisory.status`, dropping `advisory.status_id` and the `advisory_status` table (Task 2)
- SeaORM `advisory` entity updated with the `AdvisoryStatus` enum; `advisory_status` entity removed (Task 3)
- Advisory service, models, endpoints, and search queries use `advisory.status` with no join (Task 4)
- Advisory ingestion writes the enum value directly, failing closed on unknown statuses (Task 5)
- Internal architecture docs updated (Task 6)

These changes must land on `main` together: the migration and code changes are mutually dependent.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes the changes from Tasks 2–6 and links feature TC-9005

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2, 3, 4, 5, 6) have been merged into the `TC-9005` feature branch before creating the merge PR
- [ ] Verify CI on the `TC-9005` branch passes (build, migration tests, integration tests)

## Dependencies
- Depends on: Task 2 — Add atomic migration replacing advisory_status table with advisory_status_enum column
- Depends on: Task 3 — Update SeaORM advisory entity to use AdvisoryStatus enum
- Depends on: Task 4 — Update advisory queries to use status enum column instead of join
- Depends on: Task 5 — Update advisory ingestion to write status enum directly
- Depends on: Task 6 — Update internal architecture docs for advisory status enum

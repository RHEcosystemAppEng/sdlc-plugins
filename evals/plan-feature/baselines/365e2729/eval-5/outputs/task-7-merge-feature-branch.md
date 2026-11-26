**Summary:** Merge feature branch TC-9005 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks:

- Task 2 — reversible, atomic migration creating `advisory_status_enum`, adding/backfilling `advisory.status`, dropping `advisory.status_id` and the `advisory_status` table
- Task 3 — SeaORM `advisory` entity uses `AdvisoryStatus` active enum; lookup entity/relation removed
- Task 4 — advisory service, models, endpoints, SBOM and search consumers read `advisory.status` directly; status filter without join; API response shape unchanged
- Task 5 — ingestion pipeline writes enum values directly and rejects unknown statuses
- Task 6 — internal architecture docs updated

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes the changes from Tasks 2–6

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2, 3, 4, 5, 6) have been merged into the feature branch `TC-9005` before creating the merge PR
- [ ] Verify CI passes on the `TC-9005` branch head

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Add advisory status enum migration
- Depends on: Task 3 — Update SeaORM advisory entity to use AdvisoryStatus enum
- Depends on: Task 4 — Replace advisory_status joins with advisory.status column in queries and endpoints
- Depends on: Task 5 — Write advisory status enum directly in ingestion pipeline
- Depends on: Task 6 — Update internal architecture documentation for advisory status enum

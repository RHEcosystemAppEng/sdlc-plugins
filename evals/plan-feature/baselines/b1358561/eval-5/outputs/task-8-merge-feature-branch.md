**Summary:** Merge feature branch TC-9005 to main
**Epic:** TC-9005: Feature branch delivery and documentation

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: the atomic, reversible `advisory_status_enum` migration (Task 2), the SeaORM entity update (Task 3), removal of the `advisory_status` join from AdvisoryService/endpoints (Task 4) and SearchService (Task 5), direct enum writes in ingestion (Task 6), and the architecture doc update (Task 7). Note the deploy coordination requirement: the migration drops `advisory.status_id` and `advisory_status`, so the migration and the new binary must be rolled out together.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes all intermediate task changes and the deploy coordination note

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2–7) have been merged into `TC-9005` before creating the merge PR
- [ ] Verify CI on `TC-9005` is green (workspace build, migration tests, API integration tests)

## Dependencies
- Depends on: Task 2 — Add migration replacing advisory_status table with advisory_status_enum column
- Depends on: Task 3 — Update SeaORM advisory entity for status enum column
- Depends on: Task 4 — Use advisory.status column in AdvisoryService and advisory endpoints
- Depends on: Task 5 — Use advisory.status column in SearchService
- Depends on: Task 6 — Write advisory status enum directly in ingestion pipeline
- Depends on: Task 7 — Update internal architecture docs for advisory status enum

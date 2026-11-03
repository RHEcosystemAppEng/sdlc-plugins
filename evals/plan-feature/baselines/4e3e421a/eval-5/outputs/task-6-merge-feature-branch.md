# Task 6 — Merge feature branch TC-9005 to main

**Summary:** Merge feature branch TC-9005 to main
**Labels:** ai-generated-jira
**Priority:** High (inherited from TC-9005)
**Fix Versions:** RHTPA 2.0.0 (inherited from TC-9005, fixVersion scope = both)

---

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR that merges feature branch `TC-9005` into `main`. The PR description should summarize the changes from all of the feature's tasks:

- Task 2: a reversible, atomic migration that creates `advisory_status_enum`, adds and backfills `advisory.status`, drops `advisory.status_id`, and drops `advisory_status`, with a fail-closed guard against an incomplete backfill
- Task 3: the SeaORM `AdvisoryStatus` enum, removal of the `advisory_status` entity, and join-free advisory queries in the service and endpoints, with the API response shape unchanged
- Task 4: the ingestion pipeline writes enum values directly and rejects unknown statuses
- Task 5: internal architecture docs updated

All of these changes must land on `main` in this single merge. Merging the migration without the code, or the code without the migration, breaks every advisory query.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description lists every intermediate task and its change summary
- [ ] CI on the PR passes for the full workspace (`cargo check --workspace`, `cargo test --workspace`)

## Test Requirements
- [ ] Verify that all intermediate task PRs (Tasks 2, 3, 4, 5) have been merged into `TC-9005` before creating the merge PR
- [ ] Verify the full test suite passes on the `TC-9005` branch head
- [ ] Per the Feature's Customer Considerations, confirm that the migration has been tested against a production-sized dataset before the merge PR is approved

## Dependencies
- Depends on: Task 2 — Add migration converting advisory_status lookup table to advisory_status_enum column
- Depends on: Task 3 — Update SeaORM advisory entity and advisory queries to use the status enum column
- Depends on: Task 4 — Update advisory ingestion pipeline to write status enum values directly
- Depends on: Task 5 — Update internal architecture docs for advisory status enum schema change

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks:

- Task 2: atomic, reversible migration `m0002_advisory_status_enum`. It creates `advisory_status_enum`, adds and backfills `advisory.status` (fail-closed on unmapped rows), and drops `advisory.status_id` and the `advisory_status` table.
- Task 3: the SeaORM `AdvisoryStatus` enum on the `advisory` entity and removal of the `advisory_status` entity. Advisory service, endpoints, search, and SBOM-advisory queries no longer join the lookup table. Invalid status filters return 400. The API response shape is unchanged.
- Task 4: advisory ingestion writes the enum directly and rejects unknown status strings.
- Task 5: internal architecture documentation updated.

The PR description must also call out the deployment note: the migration and the new binary must roll out together, because dropping `status_id` and `advisory_status` breaks pre-TC-9005 instances. It must also note that the migration was validated against a production-sized dataset.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes Tasks 2 to 5 and includes the deployment note

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2, 3, 4, 5) have been merged into `TC-9005` before creating the merge PR
- [ ] Verify CI on `TC-9005` is green, with the full workspace build and API tests passing, before opening the PR

## Dependencies
- Depends on: Task 2 — Add advisory_status_enum migration
- Depends on: Task 3 — Update SeaORM entities and advisory query layer to use the status enum column
- Depends on: Task 4 — Write advisory status enum directly in the ingestion pipeline
- Depends on: Task 5 — Update internal architecture docs for advisory status enum

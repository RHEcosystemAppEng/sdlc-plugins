## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9005` from the latest `main`. All subsequent implementation tasks for TC-9005 (Drop status table and migrate to enum column) will target this branch.

The feature uses the feature-branch workflow because the schema migration, the SeaORM entity changes, the advisory query changes, and the ingestion pipeline changes must land on `main` together: merging the migration alone breaks every advisory query (they still join the dropped `advisory_status` table), and merging the code alone points at a `status` column that does not exist yet.

## Acceptance Criteria
- [ ] The feature branch `TC-9005` exists and is pushed to the remote
- [ ] The branch was created from the latest `main` commit

## Test Requirements
- [ ] Verify the branch `TC-9005` exists on the remote after push (e.g., `git ls-remote --heads origin TC-9005` returns one ref)

## Dependencies
- None

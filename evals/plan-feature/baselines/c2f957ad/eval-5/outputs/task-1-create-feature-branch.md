## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9005` from the latest `main`. All subsequent implementation tasks for feature TC-9005 (Drop status table and migrate to enum column) will target this branch.

This feature uses feature-branch mode because the schema migration, SeaORM entity changes, advisory query changes, and ingestion pipeline changes must all land on `main` together: merging the migration alone would break every advisory query (they still join the dropped `advisory_status` table), and merging the code alone would reference a `status` column that does not yet exist.

## Acceptance Criteria
- [ ] The feature branch `TC-9005` exists and is pushed to the remote
- [ ] The branch `TC-9005` is created from the latest `main` commit

## Test Requirements
- [ ] Verify the branch `TC-9005` exists on the remote after push (e.g., `git ls-remote --heads origin TC-9005` returns a ref)

## Dependencies
- None

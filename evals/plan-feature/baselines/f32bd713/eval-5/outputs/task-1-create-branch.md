## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9005` from the latest `main`. All subsequent implementation tasks for the "Drop status table and migrate to enum column" feature will target this branch. This ensures all changes land atomically — the migration, entity updates, service/endpoint changes, and ingestion pipeline modifications must be merged together to avoid leaving the database or application in an inconsistent state.

## Acceptance Criteria
- [ ] The feature branch `TC-9005` exists locally and is based on the latest `main`
- [ ] The feature branch `TC-9005` is pushed to the remote repository

## Test Requirements
- [ ] Verify the branch `TC-9005` exists on the remote after push (`git ls-remote --heads origin TC-9005`)
- [ ] Verify the branch is based on the current HEAD of `main`

## Dependencies
None

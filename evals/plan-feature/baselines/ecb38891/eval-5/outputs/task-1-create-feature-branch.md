## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9005` from the latest `main`. All subsequent implementation tasks for the "Drop status table and migrate to enum column" feature will target this branch. This ensures all changes land atomically -- the database migration, entity updates, service layer changes, ingestion pipeline updates, and test updates must all be merged together to avoid leaving the database or codebase in an inconsistent state.

## Acceptance Criteria
- [ ] Feature branch `TC-9005` exists locally and is pushed to the remote
- [ ] Branch is created from the latest `main` HEAD

## Test Requirements
- [ ] Verify the branch `TC-9005` exists on the remote after push (`git ls-remote --heads origin TC-9005`)

## Dependencies
- None (this is the first task)

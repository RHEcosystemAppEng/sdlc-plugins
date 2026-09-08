## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9005` from the latest `main`. All subsequent implementation tasks will target this branch. This feature requires atomic delivery because the database migration, entity definitions, service/endpoint changes, and ingestion pipeline updates are tightly coupled -- partial delivery to `main` would break the application.

## Acceptance Criteria
- [ ] The feature branch `TC-9005` exists and is pushed to the remote
- [ ] The branch is created from the latest `main`

## Test Requirements
- [ ] Verify the branch `TC-9005` exists on the remote after push
- [ ] Verify the branch point matches the HEAD of `main` at creation time

## Dependencies
None

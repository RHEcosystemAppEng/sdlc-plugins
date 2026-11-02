## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9005` from the latest `main`. All subsequent implementation tasks will target this branch. This feature requires all changes to land together — the database migration, entity updates, service/endpoint changes, and ingestion pipeline updates are interdependent and cannot be merged independently to `main`.

## Acceptance Criteria
- [ ] Feature branch `TC-9005` exists and is pushed to the remote
- [ ] Branch is created from the latest `main` commit

## Test Requirements
- [ ] Verify the branch `TC-9005` exists on the remote after push
- [ ] Verify the branch point matches the latest `main` commit

## Dependencies
- None — this is the first task in the feature-branch workflow

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9005` from the latest `main`. All subsequent implementation tasks for the advisory status enum migration will target this branch. This feature requires all changes to land together (migration, entity updates, service/endpoint changes, and ingestion pipeline updates), so a feature branch is used to coordinate delivery.

## Acceptance Criteria
- [ ] The feature branch `TC-9005` exists locally and is pushed to the remote
- [ ] The branch is based on the latest `main`

## Test Requirements
- [ ] Verify the branch exists on the remote after push (`git ls-remote --heads origin TC-9005`)

## Dependencies
- None (this is the first task)

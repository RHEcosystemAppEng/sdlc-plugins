## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9005` from the latest `main`. All subsequent implementation tasks for the advisory status enum migration will target this branch. This feature requires all changes to land atomically — the database migration, entity updates, service layer changes, ingestion pipeline updates, and test modifications must all be merged together to avoid leaving the database or application in an inconsistent state.

## Acceptance Criteria
- [ ] Feature branch `TC-9005` exists on the remote repository
- [ ] Branch is created from the latest `main` commit

## Test Requirements
- [ ] Verify the branch `TC-9005` exists on the remote after push (`git ls-remote --heads origin TC-9005`)

## Dependencies
- None

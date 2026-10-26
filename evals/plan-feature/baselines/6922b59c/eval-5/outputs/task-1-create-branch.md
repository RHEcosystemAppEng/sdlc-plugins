## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9005` from the latest `main`. All subsequent implementation tasks will target this branch. This branch is required because the feature involves coordinated schema migrations and tightly coupled code changes that must land atomically — merging the migration without the code changes would break all advisory queries, and merging the code changes without the migration would reference a column that does not exist.

## Acceptance Criteria
- [ ] The feature branch `TC-9005` exists locally and is pushed to the remote
- [ ] The branch is created from the latest `main` commit

## Test Requirements
- [ ] Verify the branch `TC-9005` exists on the remote after push (`git ls-remote --heads origin TC-9005` returns a result)

## Dependencies
None

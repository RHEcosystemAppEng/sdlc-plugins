## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9005` from the latest `main`. All subsequent implementation tasks will target this branch. This feature requires atomic delivery because the database migration, entity definitions, service layer changes, and ingestion pipeline updates are tightly coupled -- merging any subset independently would leave the codebase or database in an inconsistent state.

## Acceptance Criteria
- [ ] Feature branch `TC-9005` exists locally and is pushed to the remote
- [ ] Branch is created from the latest `main` commit

## Test Requirements
- [ ] Verify the branch `TC-9005` exists on the remote after push (`git ls-remote --heads origin TC-9005`)

## Dependencies
None

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9005` from the latest `main`. All subsequent implementation tasks will target this branch. This feature migrates the `advisory_status` lookup table to a PostgreSQL enum column on the `advisory` table, requiring all changes to land atomically.

## Acceptance Criteria
- [ ] The feature branch `TC-9005` exists locally and is pushed to the remote
- [ ] The branch is created from the latest `main` commit

## Test Requirements
- [ ] Verify the branch `TC-9005` exists on the remote after push (`git ls-remote --heads origin TC-9005`)

## Dependencies
None

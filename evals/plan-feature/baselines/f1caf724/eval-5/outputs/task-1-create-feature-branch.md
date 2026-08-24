## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9005` from the latest `main`. All subsequent implementation tasks for the advisory status enum migration will target this branch. This feature requires atomic delivery because the database migration and code changes are tightly coupled — partial merges would leave the database or application in an inconsistent state.

## Acceptance Criteria
- [ ] Feature branch `TC-9005` exists locally and is based on the latest `main`
- [ ] Feature branch `TC-9005` is pushed to the remote

## Test Requirements
- [ ] Verify the branch `TC-9005` exists on the remote after push
- [ ] Verify the branch is based on the latest `main` commit

## Dependencies
None

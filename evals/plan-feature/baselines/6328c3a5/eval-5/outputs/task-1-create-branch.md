## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9005` from the latest `main`. All subsequent implementation tasks will target this branch. This feature implements the advisory status enum migration, which requires all changes to land atomically -- the feature branch ensures coordinated delivery.

## Acceptance Criteria
- [ ] Feature branch `TC-9005` exists locally and is pushed to the remote
- [ ] Branch is created from the latest `main` commit

## Test Requirements
- [ ] Verify the branch `TC-9005` exists on the remote after push (`git ls-remote --heads origin TC-9005`)

## Dependencies
None

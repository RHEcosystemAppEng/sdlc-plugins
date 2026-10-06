## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9005` from the latest `main`. All subsequent implementation tasks for the advisory status enum migration will target this branch. This feature requires all changes (migration, entity updates, service updates, ingestion updates, tests) to land together atomically, so a feature branch is used to accumulate all PRs before merging to main.

## Acceptance Criteria
- [ ] Feature branch `TC-9005` exists on the remote repository
- [ ] Branch is created from the latest `main` commit

## Test Requirements
- [ ] Verify the branch `TC-9005` exists on the remote after push (`git ls-remote --heads origin TC-9005`)

## Dependencies
None

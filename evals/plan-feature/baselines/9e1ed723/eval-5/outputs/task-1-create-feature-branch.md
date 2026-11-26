**Summary:** Create feature branch TC-9005 from main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9005` from the latest `main`. All subsequent implementation tasks will target this branch.

TC-9005 replaces the `advisory_status` lookup table with an `advisory_status_enum` column on `advisory`. The migration, entity, query and ingestion changes must land on `main` together. Merging any one of them alone breaks advisory queries. Those changes are collected on this branch and merged once by the closing bookend task.

## Acceptance Criteria
- [ ] The feature branch `TC-9005` exists and is pushed to the remote
- [ ] `TC-9005` is created from the latest `main` commit

## Test Requirements
- [ ] Verify the branch exists on the remote after push (e.g., `git ls-remote --heads origin TC-9005` returns a ref)

## Dependencies
- None

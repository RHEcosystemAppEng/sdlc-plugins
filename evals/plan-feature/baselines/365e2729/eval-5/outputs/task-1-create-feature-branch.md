**Summary:** Create feature branch TC-9005 from main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9005` from the latest `main`. All subsequent implementation tasks will target this branch.

TC-9005 replaces the `advisory_status` lookup table with an `advisory_status_enum` column on `advisory`. The migration, entity, query, and ingestion changes must land together (merging any one alone breaks advisory queries), so they are developed on this feature branch and merged to `main` as a single unit.

## Acceptance Criteria
- [ ] The feature branch `TC-9005` exists and is pushed to the remote
- [ ] `TC-9005` is created from the latest `main` commit

## Test Requirements
- [ ] Verify the branch `TC-9005` exists on the remote after push (e.g., `git ls-remote --heads origin TC-9005` returns a ref)

## Dependencies
- None

**Summary:** Create feature branch TC-9005 from main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9005` from the latest `main`. All subsequent implementation tasks will target this branch.

TC-9005 (Drop status table and migrate to enum column) needs all-or-nothing delivery. The schema migration drops `advisory.status_id` and the `advisory_status` table. The SeaORM entity, the advisory query and service layer, and the ingestion pipeline all depend on that schema. If any one of these lands on `main` alone, advisory queries break. The intermediate tasks are merged into `TC-9005` first. The branch then merges to `main` in one step (see the merge-branch bookend task).

## Acceptance Criteria
- [ ] The feature branch `TC-9005` exists and is pushed to the remote
- [ ] The branch is created from the latest `main` commit

## Test Requirements
- [ ] Verify the branch `TC-9005` exists on the remote after push (e.g., `git ls-remote --heads origin TC-9005` returns one ref)

## Dependencies
- None

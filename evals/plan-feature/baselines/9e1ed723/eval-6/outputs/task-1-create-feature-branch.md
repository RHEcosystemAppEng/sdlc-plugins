# Task 1 — Create feature branch TC-9006 from main

**Summary:** Create feature branch TC-9006 from main
**Parent Epic:** TC-9006: trustify-backend (Epic group "trustify-backend")

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9006` from the latest `main`. All subsequent implementation tasks will target this branch.

This feature runs in `feature-branch` mode because the new `/remediation` dashboard in trustify-ui needs new backend aggregation endpoints that do not exist yet (tightly coupled frontend/backend components). See the workflow mode decision comment on TC-9006.

Cross-repository note: the frontend tasks (Tasks 5–7, repository trustify-ui) also target `TC-9006`. Per the bookend rules this task names one repository (trustify-backend, which has most of the tasks). Before Task 5 starts, the implementer must also make sure a `TC-9006` branch exists in trustify-ui (see "Open questions" in the impact map).

## Acceptance Criteria
- [ ] The feature branch `TC-9006` exists in trustify-backend and is pushed to the remote, created from the latest `main`

## Test Requirements
- [ ] Verify the branch `TC-9006` exists on the remote after the push (e.g., `git ls-remote --heads origin TC-9006` returns one ref)

## Dependencies
- None

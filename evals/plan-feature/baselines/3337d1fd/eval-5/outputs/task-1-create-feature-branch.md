## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9005` from the latest `main`. All subsequent implementation tasks for the advisory status enum migration will target this branch. The feature-branch workflow is required because the database migration, entity changes, service layer updates, and ingestion pipeline changes are tightly coupled — merging any subset without the others would leave the database or application in an inconsistent state.

## Acceptance Criteria
- [ ] Feature branch `TC-9005` exists locally and is based on the latest `main`
- [ ] Feature branch `TC-9005` is pushed to the remote repository

## Test Requirements
- [ ] Verify the branch `TC-9005` exists on the remote after push (`git ls-remote --heads origin TC-9005`)

## Dependencies
None — this is the first task in the feature-branch workflow.

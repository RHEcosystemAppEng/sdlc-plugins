# Task 1 — Create feature branch TC-9005 from main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9005` from the latest `main`. All subsequent implementation tasks will target this branch. This feature branch is needed because the advisory status migration from lookup table to enum column requires all changes to land together — the database migration, entity definitions, service layer, endpoints, and ingestion pipeline are tightly coupled and cannot be merged independently to `main`.

## Acceptance Criteria
- [ ] Feature branch `TC-9005` exists and is pushed to the remote

## Test Requirements
- [ ] Verify the branch `TC-9005` exists on the remote after push

## Dependencies
None — this is the first task in the feature-branch workflow.

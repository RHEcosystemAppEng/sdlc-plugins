# Task 1 — Create feature branch TC-9005 from main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9005` from the latest `main`. All subsequent implementation tasks for the "Drop status table and migrate to enum column" feature will target this branch. This ensures all changes land atomically — the migration, entity updates, service/endpoint changes, and ingestion pipeline updates must be merged together to avoid leaving the database or application in an inconsistent state.

## Acceptance Criteria
- [ ] The feature branch `TC-9005` exists on the remote repository
- [ ] The branch is created from the latest `main` commit

## Test Requirements
- [ ] Verify the branch `TC-9005` exists on the remote after push (`git ls-remote --heads origin TC-9005`)

## Dependencies
- None (this is the first task)

[sdlc-workflow] Description digest: sha256-md:35c1e2194e0fb15fdd59ba8ab79abdfa1d579dca9ee8745d34b025f2695aaf17

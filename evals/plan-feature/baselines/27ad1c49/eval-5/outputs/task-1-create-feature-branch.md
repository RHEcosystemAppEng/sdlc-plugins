## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create feature branch TC-9005 from main to isolate all changes for the advisory status enum migration. This feature has atomicity constraints: the database migration, entity updates, service/endpoint changes, and ingestion pipeline changes must all land together. Merging any subset independently would leave the application in a broken state (queries referencing a dropped table, or code referencing a non-existent column). The feature branch ensures all changes are developed and reviewed together before being merged atomically to main.

## Acceptance Criteria
- [ ] Feature branch TC-9005 is created from the latest main branch in trustify-backend
- [ ] Branch is pushed to the remote repository
- [ ] Branch name matches the feature issue key exactly: TC-9005

## Test Requirements
- [ ] Verify the branch exists on the remote with `git ls-remote --heads origin TC-9005`
- [ ] Verify the branch point matches the current main HEAD

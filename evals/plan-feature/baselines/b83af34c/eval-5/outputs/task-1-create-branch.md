## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create the feature branch TC-9005 from main to support atomic delivery of the advisory status enum migration. All implementation tasks for this feature will target this branch, ensuring the database migration, entity updates, service changes, and ingestion pipeline changes land together when the branch is merged back to main.

## Acceptance Criteria
- [ ] Feature branch TC-9005 is created from the latest main
- [ ] Branch is pushed to the remote repository
- [ ] Branch name matches the feature issue ID: TC-9005

## Test Requirements
- [ ] Verify the branch exists on the remote after push
- [ ] Verify the branch point matches the HEAD of main at creation time

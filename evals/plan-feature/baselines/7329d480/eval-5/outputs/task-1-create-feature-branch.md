# Task 1: Create feature branch TC-9005 from main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create the feature branch `TC-9005` from `main` to isolate all changes for the advisory status enum migration. This feature requires atomic delivery because the database migration, entity updates, service changes, and ingestion pipeline updates are interdependent — merging any subset independently would leave the application in a broken state.

## Acceptance Criteria
- [ ] Feature branch `TC-9005` exists and is based on the latest `main`
- [ ] Branch is pushed to the remote repository
- [ ] Subsequent tasks can target `TC-9005` as their base branch

## Test Requirements
- [ ] Branch exists on remote and is reachable by CI

## Dependencies
- None (this is the first task)

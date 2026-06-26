## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create PR to merge feature branch TC-9005 into main. This brings all the advisory status enum migration changes together atomically: the database migration, entity updates, service/endpoint changes, ingestor updates, and test updates all land in a single merge.

## Acceptance Criteria
- [ ] PR from TC-9005 to main is open and ready for review

## Test Requirements
- [ ] Verify all intermediate task PRs merged into feature branch

## Dependencies
- Depends on: Task 2 -- Database migration for advisory_status_enum
- Depends on: Task 3 -- Update SeaORM entity definitions
- Depends on: Task 4 -- Update advisory service and endpoints
- Depends on: Task 5 -- Update advisory ingestor
- Depends on: Task 6 -- Update integration tests

[sdlc-workflow] Description digest: sha256-md:69a95dc5b2e646aa4ffb4d9f07eb2b55101991cfd7953f8feb516f681f2a23c3

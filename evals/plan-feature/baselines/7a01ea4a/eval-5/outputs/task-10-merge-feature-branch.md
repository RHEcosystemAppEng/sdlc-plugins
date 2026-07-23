## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: database migration from lookup table to enum column, entity definition updates, model/service/endpoint updates, ingestion pipeline changes, integration test updates, and documentation updates. This PR represents the atomic delivery of the "Drop status table and migrate to enum column" feature.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] PR description summarizes all changes from all intermediate tasks
- [ ] All CI checks pass on the feature branch

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify the full test suite passes on the feature branch (`cargo test`)
- [ ] Verify the migration runs cleanly on a fresh database

## Dependencies
- Depends on: Task 2 -- Create migration for advisory_status_enum
- Depends on: Task 3 -- Update SeaORM entity definitions
- Depends on: Task 4 -- Update advisory models
- Depends on: Task 5 -- Update AdvisoryService
- Depends on: Task 6 -- Update advisory endpoints
- Depends on: Task 7 -- Update ingestion pipeline
- Depends on: Task 8 -- Update integration tests
- Depends on: Task 9 -- Documentation updates

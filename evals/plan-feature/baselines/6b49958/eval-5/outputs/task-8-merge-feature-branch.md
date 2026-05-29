## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: database migration from lookup table to enum column, entity definition updates, service and endpoint query changes, ingestion pipeline simplification, and integration test updates.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes all changes from tasks 2 through 7

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR

## Dependencies
- Depends on: Task 2 — Create migration for advisory_status_enum
- Depends on: Task 3 — Update SeaORM entity definitions
- Depends on: Task 4 — Update advisory service and models
- Depends on: Task 5 — Update advisory endpoints
- Depends on: Task 6 — Update ingestion pipeline
- Depends on: Task 7 — Update integration tests

[sdlc-workflow] Description digest: sha256:c3f54de0658b041197a872ce72a839d94c33175d38516a08f104956b55f670a5

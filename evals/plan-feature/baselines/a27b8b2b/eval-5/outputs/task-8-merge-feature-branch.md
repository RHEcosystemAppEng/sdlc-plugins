## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: database migration from `advisory_status` lookup table to `advisory_status_enum` column, entity definition updates, service/endpoint query simplification, ingestion pipeline updates, test updates, and documentation updates. This PR delivers all changes atomically as required by the feature's non-functional requirements.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] PR description summarizes all changes across the feature's implementation tasks
- [ ] All CI checks pass on the PR

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify the feature branch is up to date with `main` (rebase or merge main into the feature branch if needed)
- [ ] Verify all tests pass on the feature branch

## Dependencies
- Depends on: Task 2 — Create migration for advisory status enum
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and endpoints
- Depends on: Task 5 — Update advisory ingestion pipeline
- Depends on: Task 6 — Update advisory integration tests
- Depends on: Task 7 — Update internal architecture documentation

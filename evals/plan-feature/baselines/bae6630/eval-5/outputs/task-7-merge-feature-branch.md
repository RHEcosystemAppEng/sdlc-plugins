## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a pull request to merge feature branch TC-9005 into main. This delivers the complete advisory status enum migration as a single atomic change: the database migration, entity updates, service/model changes, ingestion pipeline updates, and endpoint/test updates all land together, preventing any intermediate broken state.

## Acceptance Criteria
- [ ] PR is created from TC-9005 to main
- [ ] All CI checks pass on the PR
- [ ] All intermediate task PRs have been merged to TC-9005
- [ ] No references to `advisory_status` lookup table remain in the codebase

## Test Requirements
- [ ] Full test suite passes on the TC-9005 branch before merge
- [ ] Advisory integration tests pass end-to-end with the enum-based schema

## Dependencies
- Depends on: Task 2 — Create database migration for advisory status enum
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and model layer to use status enum
- Depends on: Task 5 — Update advisory ingestion pipeline for direct enum writes
- Depends on: Task 6 — Update advisory endpoints and integration tests

## Digest
[sdlc-workflow] Description digest: sha256-md:659be62d21545131a7c1bf9e097225ecc328f3c563ad15eacb2dd75036c7882e

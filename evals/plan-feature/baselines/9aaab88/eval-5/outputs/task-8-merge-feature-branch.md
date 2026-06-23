## Repository
trustify-backend

## Bookend Type
merge-branch

## Target Branch
main

## Description
Merge feature branch TC-9005 to main after all intermediate tasks are complete and verified. This merge delivers all advisory status enum migration changes atomically — the database migration, entity updates, service layer changes, endpoint modifications, ingestion pipeline updates, and integration tests all land together in a single merge to main, preventing any inconsistent intermediate state.

## Acceptance Criteria
- [ ] All intermediate tasks (Tasks 2-7) are complete and their PRs are merged to TC-9005
- [ ] All tests pass on the TC-9005 branch
- [ ] Feature branch TC-9005 is merged to main via pull request
- [ ] No merge conflicts with main
- [ ] CI pipeline passes on the merge commit

## Test Requirements
- [ ] Full test suite passes on the merged main branch
- [ ] Advisory list endpoint returns correct status values after merge
- [ ] Advisory ingestion writes enum values correctly after merge

## Dependencies
- Depends on: Task 2 — Create advisory status enum migration
- Depends on: Task 3 — Update SeaORM entity definitions for enum status
- Depends on: Task 4 — Update advisory service and model layer
- Depends on: Task 5 — Update advisory endpoints for enum status filtering
- Depends on: Task 6 — Update advisory ingestion pipeline for enum status
- Depends on: Task 7 — Add integration tests for enum status migration

[sdlc-workflow] Description digest: sha256-md:0f07fbf5e228485592a367c027b309045128eeaad912910837551f9fce862994

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Merge feature branch TC-9005 to main. All intermediate tasks (migration, entity updates, service/model updates, endpoint/ingestion updates, and integration tests) have been completed and verified on the feature branch. This merge delivers the complete atomic change set — enum migration plus all code changes — to main, ensuring no partial state is ever visible.

## Acceptance Criteria
- [ ] All intermediate tasks (Tasks 2-6) are complete and verified on branch TC-9005
- [ ] All CI checks pass on the feature branch before merge
- [ ] Feature branch TC-9005 is merged to main via pull request
- [ ] No merge conflicts with main
- [ ] Post-merge CI pipeline passes on main

## Test Requirements
- [ ] All integration tests pass on the feature branch before merge
- [ ] Post-merge test suite passes on main
- [ ] Advisory list endpoint works correctly on the merged main branch

## Dependencies
- Depends on: Task 2 — Create migration for advisory_status_enum
- Depends on: Task 3 — Update entity definitions
- Depends on: Task 4 — Update advisory service and models
- Depends on: Task 5 — Update advisory endpoints and ingestion
- Depends on: Task 6 — Update integration tests

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Merge feature branch TC-9005 to main, delivering all advisory status enum migration changes atomically. This merge brings together the database migration, entity definition updates, service/endpoint changes, and ingestion pipeline updates as a single atomic delivery. All intermediate tasks must be complete and their PRs merged to the TC-9005 branch before this merge proceeds. The atomicity constraint is satisfied: main never sees a partial state where the migration exists without the code changes or vice versa.

## Acceptance Criteria
- [ ] All intermediate task PRs have been merged to the TC-9005 branch
- [ ] TC-9005 branch passes all CI checks (build, tests, linting)
- [ ] Feature branch TC-9005 is merged to main via pull request
- [ ] No merge conflicts with main
- [ ] All advisory-related tests pass on the merged main branch
- [ ] The `advisory_status` table join is fully eliminated from the codebase

## Test Requirements
- [ ] Full test suite passes on the merged result before merge completes
- [ ] Advisory list endpoint integration tests pass with enum-based status
- [ ] Advisory ingestion tests pass with direct enum writes
- [ ] Migration tests pass (up and down migrations)

## Dependencies
- Depends on: Task 2 — Create database migration for advisory status enum
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and endpoints to use enum column
- Depends on: Task 5 — Update advisory ingestion pipeline for enum status

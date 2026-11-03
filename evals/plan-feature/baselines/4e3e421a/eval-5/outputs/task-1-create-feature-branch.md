# Task 1 — Create feature branch TC-9005 from main

**Summary:** Create feature branch TC-9005 from main
**Labels:** ai-generated-jira
**Priority:** High (inherited from TC-9005)
**Fix Versions:** RHTPA 2.0.0 (inherited from TC-9005, fixVersion scope = both)

---

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9005` from the latest `main`. All subsequent implementation tasks will target this branch.

TC-9005 replaces the `advisory_status` lookup table with a PostgreSQL enum column on `advisory`. The schema migration, the SeaORM entity changes, the advisory query changes, and the ingestion pipeline changes cannot be merged to `main` separately. Merging the migration alone breaks every advisory query, because they still join the dropped table. Merging the code changes alone references a `status` column that does not exist. All work is therefore collected on this feature branch and merged to `main` in a single PR (Task 6).

## Acceptance Criteria
- [ ] The feature branch `TC-9005` exists and is pushed to the remote
- [ ] The branch is created from the latest `main` HEAD at the time of creation

## Test Requirements
- [ ] Verify the branch exists on the remote after push (e.g., `git ls-remote --heads origin TC-9005` returns one ref)

## Dependencies
- None

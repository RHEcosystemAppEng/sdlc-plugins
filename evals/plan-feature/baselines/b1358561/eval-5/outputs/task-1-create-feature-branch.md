**Summary:** Create feature branch TC-9005 from main
**Epic:** TC-9005: Feature branch delivery and documentation

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9005` from the latest `main`. All subsequent implementation tasks will target this branch. Feature TC-9005 (Drop status table and migrate to enum column) requires all schema and code changes to land together, so they are accumulated on `TC-9005` and merged to `main` in a single PR.

## Acceptance Criteria
- [ ] The feature branch `TC-9005` exists and is pushed to the remote
- [ ] `TC-9005` is created from the latest `main`

## Test Requirements
- [ ] Verify the branch `TC-9005` exists on the remote after push (e.g., `git ls-remote --heads origin TC-9005` returns a ref)

## Dependencies
- None

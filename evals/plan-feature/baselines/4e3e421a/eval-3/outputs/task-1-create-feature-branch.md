# Task 1 — Create feature branch TC-9003 from main

## Repository
trustify-ui

## Target Branch
main

## Bookend Type
create-branch

## Description
Create the feature branch `TC-9003` from the latest `main` and push it. All later implementation tasks for TC-9003 (SBOM comparison view) target this branch. The feature uses `feature-branch` mode because the new comparison UI depends on a new backend endpoint and cannot ship to `main` by itself.

## Acceptance Criteria
- [ ] The feature branch `TC-9003` exists and is pushed to the remote

## Test Requirements
- [ ] After the push, verify the branch exists on the remote (e.g., `git ls-remote --heads origin TC-9003` returns one ref)

## Dependencies
- None

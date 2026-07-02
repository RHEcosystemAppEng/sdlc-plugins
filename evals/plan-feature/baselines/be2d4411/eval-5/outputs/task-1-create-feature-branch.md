## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9005` from the latest `main`. All subsequent implementation tasks for the advisory status enum migration will target this branch. This feature requires feature-branch mode because the database migration and all code changes are tightly coupled — merging any subset independently would leave `main` in a broken state.

## Acceptance Criteria
- [ ] Feature branch `TC-9005` exists locally and is pushed to the remote
- [ ] Branch is created from the latest `main` commit

## Test Requirements
- [ ] Verify the branch `TC-9005` exists on the remote after push (`git ls-remote --heads origin TC-9005`)

## Dependencies
None — this is the first task.

## Labels
- ai-generated-jira

## additional_fields
- priority: High
- fixVersions: RHTPA 2.0.0

[sdlc-workflow] Description digest: sha256-md:9d3faea19338ddea41e0f72d2bfabdb1cf3e8e4a5fac29126c75fb778c896d90

## Summary
Create feature branch TC-9005 from main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push feature branch TC-9005 from latest main. This branch will serve as the integration branch for all intermediate tasks in the TC-9005 feature (drop advisory_status table and migrate to enum column). All intermediate task PRs will target this feature branch instead of main, ensuring that tightly coupled migration and code changes land together atomically.

## Acceptance Criteria
- [ ] Branch TC-9005 exists locally, created from the latest main
- [ ] Branch TC-9005 is pushed to the remote repository

## Test Requirements
- [ ] Verify branch TC-9005 exists on remote after push (`git ls-remote --heads origin TC-9005`)

## Dependencies
None

[sdlc-workflow] Description digest: sha256-md:4131636120bd053fb98394b88f37434ec2d49a51a6e5556d80b52091d5c6e12a

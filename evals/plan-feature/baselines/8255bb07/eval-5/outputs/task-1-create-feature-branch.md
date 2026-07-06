## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9005` from the latest `main`. All subsequent implementation tasks will target this branch. This feature migrates the `advisory_status` lookup table to an enum column on the `advisory` table. All changes must land atomically because the migration, entity definitions, service layer, and ingestion pipeline are tightly coupled.

## Acceptance Criteria
- [ ] The feature branch `TC-9005` exists and is pushed to the remote

## Test Requirements
- [ ] Verify the branch `TC-9005` exists on the remote after push

## Dependencies
None

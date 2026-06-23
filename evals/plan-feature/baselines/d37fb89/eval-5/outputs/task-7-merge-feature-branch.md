## Summary
Merge feature branch TC-9005 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a pull request to merge feature branch TC-9005 into main. This PR consolidates all intermediate task changes: the database migration (advisory status enum), updated entity definitions, updated advisory service/endpoints, updated ingestion pipeline, and updated integration tests. All changes must land together to maintain schema-code consistency.

## Acceptance Criteria
- [ ] A PR from TC-9005 to main is open and ready for review
- [ ] All intermediate task PRs have been merged into the TC-9005 feature branch
- [ ] CI passes on the feature branch

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2-6) have been merged into the TC-9005 feature branch
- [ ] Verify CI pipeline passes on the TC-9005 branch before opening the PR

## Dependencies
- Depends on: Task 2 -- Create database migration for advisory status enum
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 -- Update advisory service and endpoints to use status enum column
- Depends on: Task 5 -- Update advisory ingestion pipeline to write enum status directly
- Depends on: Task 6 -- Update advisory integration tests for status enum migration

[sdlc-workflow] Description digest: sha256-md:05bf6a8e96151d3effa7414beabc1dcd5c2239a56c5e892b00074cbc6f1dde33

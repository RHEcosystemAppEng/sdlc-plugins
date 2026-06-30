## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch TC-9005 into main. The PR description should summarize all changes made across the feature's tasks: database migration from advisory_status lookup table to advisory_status_enum column, updated entity definitions, refactored advisory service/endpoints, updated ingestion pipeline, and updated integration tests.

## Acceptance Criteria
- [ ] A PR from TC-9005 to main is open and ready for review

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch TC-9005 before creating the merge PR

## Dependencies
- Depends on: Task 2 -- Database migration
- Depends on: Task 3 -- Entity definitions update
- Depends on: Task 4 -- Advisory service/endpoints update
- Depends on: Task 5 -- Ingestion pipeline update
- Depends on: Task 6 -- Integration tests

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "High"}, "fixVersions": [{"name": "RHTPA 2.0.0"}]}

[sdlc-workflow] Description digest: sha256-md:b744ddf518db7fe12fbb8e4905240cc2db12f650dcdbe65ac107730af1b8f819

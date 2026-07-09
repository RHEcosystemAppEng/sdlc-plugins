## Repository
trustify-ui

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: the new SBOM comparison backend endpoint, frontend comparison page with diff sections, export functionality, tests, and documentation. This PR consolidates the complete SBOM comparison view feature for final review and delivery.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review
- [ ] PR description summarizes all changes: backend comparison service and endpoint, frontend comparison page, export functionality, test coverage, and documentation
- [ ] All CI checks pass on the feature branch

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify the feature branch contains all expected changes from Tasks 2-8

## Dependencies
- Depends on: Task 2 -- Implement SBOM comparison diff model and service
- Depends on: Task 3 -- Add SBOM comparison REST endpoint with integration tests
- Depends on: Task 4 -- Add SBOM comparison API types and data-fetching hook
- Depends on: Task 5 -- Implement SBOM comparison page with diff sections
- Depends on: Task 6 -- Add export functionality for comparison results
- Depends on: Task 7 -- Add tests for SBOM comparison page
- Depends on: Task 8 -- Document SBOM comparison endpoint and UI workflow

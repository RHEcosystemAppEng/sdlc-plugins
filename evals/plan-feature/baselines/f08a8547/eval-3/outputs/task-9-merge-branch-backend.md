## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main` in the trustify-backend repository. The PR description should summarize all backend changes made across the feature's tasks: the SBOM comparison diff model structs, the comparison service, and the comparison REST endpoint.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open in the trustify-backend repository and ready for review
- [ ] PR description summarizes all backend changes: comparison model, service, and endpoint
- [ ] All intermediate backend task PRs have been merged into the TC-9003 feature branch

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2, 3) have been merged into the feature branch before creating the merge PR
- [ ] Verify the feature branch builds and all tests pass before opening the PR

## Dependencies
- Depends on: Task 2 — Add SBOM comparison diff model and service
- Depends on: Task 3 — Add SBOM comparison REST endpoint with integration tests

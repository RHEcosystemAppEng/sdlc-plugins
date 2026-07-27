## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: the backend SBOM comparison model, service, and endpoint (Tasks 2-3), the frontend API layer, comparison page UI, and routing integration (Tasks 4-6), and the feature documentation (Task 7). This covers changes in both the trustify-backend and trustify-ui repositories.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review in trustify-backend
- [ ] A PR from `TC-9003` to `main` is open and ready for review in trustify-ui
- [ ] PR descriptions summarize all changes from Tasks 2-7
- [ ] All CI checks pass on both PRs

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2-7) have been merged into the feature branch before creating the merge PRs
- [ ] Verify no merge conflicts exist between the feature branch and main in either repository
- [ ] Verify CI pipelines pass on the merge PRs

## Dependencies
- Depends on: Task 2 -- Add SBOM comparison model and service
- Depends on: Task 3 -- Add SBOM comparison endpoint
- Depends on: Task 4 -- Add SBOM comparison API layer
- Depends on: Task 5 -- Implement SBOM comparison page UI
- Depends on: Task 6 -- Add comparison route and SBOM list page integration
- Depends on: Task 7 -- Documentation

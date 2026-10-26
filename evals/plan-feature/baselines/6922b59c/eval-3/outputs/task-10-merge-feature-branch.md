## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: new SBOM comparison backend endpoint (`GET /api/v2/sbom/compare`), comparison model types, frontend comparison page UI with PatternFly components, SBOM list page selection, export functionality, and documentation updates.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review
- [ ] PR description summarizes all changes from the feature's implementation tasks
- [ ] All CI checks pass on the PR

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch `TC-9003` before creating the merge PR
- [ ] Verify the feature branch is up to date with `main` (rebase or merge main into the feature branch if needed)

## Dependencies
- Depends on: Task 2 — Add SBOM comparison model types
- Depends on: Task 3 — Add SBOM comparison service and REST endpoint
- Depends on: Task 4 — Add SBOM comparison endpoint integration tests
- Depends on: Task 5 — Add SBOM comparison API client and React Query hook
- Depends on: Task 6 — Build SBOM comparison page UI
- Depends on: Task 7 — Add comparison route and SBOM list selection
- Depends on: Task 8 — Add SBOM comparison export (JSON/CSV)
- Depends on: Task 9 — Update documentation for SBOM comparison feature

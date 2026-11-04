# Task 1 — Create feature branch TC-9003 from main

## Repository
trustify-ui

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9003` from the latest `main`. All subsequent implementation tasks for TC-9003 (SBOM comparison view) will target this branch. Feature-branch mode was selected because the new `/sbom/compare` UI page cannot work without the new `GET /api/v2/sbom/compare` backend endpoint (tightly coupled feature components).

Note: backend tasks (Tasks 2, 3, 9) target `TC-9003` in `trustify-backend`. See the cross-repo caveat in the workflow mode decision comment on TC-9003.

## Acceptance Criteria
- [ ] Feature branch `TC-9003` exists and is pushed to the remote of `trustify-ui`
- [ ] The branch is created from the latest `main`

## Test Requirements
- [ ] Verify the branch `TC-9003` exists on the remote after push (e.g., `git ls-remote --heads origin TC-9003` returns a ref)

## Dependencies
- None

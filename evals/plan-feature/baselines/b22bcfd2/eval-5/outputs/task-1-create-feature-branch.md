## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push feature branch TC-9005 from main. This branch will contain all changes for the "Drop status table and migrate to enum column" feature. Feature-branch workflow is required because the NFRs mandate atomic migration and coordinated code changes — all changes must land together to avoid inconsistent state.

## Acceptance Criteria
- [ ] Feature branch `TC-9005` exists on the remote, branched from the latest `main`
- [ ] Branch is pushed and accessible for subsequent tasks
- [ ] No changes are included in the branch — it is a clean copy of `main`

## Test Requirements
- [ ] Verify branch `TC-9005` exists on the remote with `git ls-remote --heads origin TC-9005`
- [ ] Verify branch HEAD matches current `main` HEAD

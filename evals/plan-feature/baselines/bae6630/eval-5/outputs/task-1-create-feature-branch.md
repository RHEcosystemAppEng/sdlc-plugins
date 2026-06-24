## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push feature branch TC-9005 from latest main. This branch will collect all changes for the advisory status enum migration (TC-9005) before merging back to main as a single unit, ensuring atomicity across the database migration and code changes.

## Acceptance Criteria
- [ ] Feature branch TC-9005 exists and is pushed to the remote
- [ ] Branch is created from the latest main

## Test Requirements
- [ ] Verify branch TC-9005 exists on the remote with `git ls-remote --heads origin TC-9005`

## Dependencies
- None

## Digest
[sdlc-workflow] Description digest: sha256-md:87e8f8e93254741ebe5d5d1039901e0178c0202198fe311aee01e3bf89bc70d1

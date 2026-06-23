## Repository
trustify-backend

## Bookend Type
create-branch

## Target Branch
main

## Description
Create feature branch TC-9005 from main to isolate all changes for the advisory status enum migration. This feature requires atomic delivery — the database migration, entity changes, service updates, endpoint modifications, and ingestion pipeline changes must all land together. A partial merge would leave the database in an inconsistent state (e.g., enum column exists but queries still join the dropped lookup table, or vice versa).

## Acceptance Criteria
- [ ] Feature branch TC-9005 exists and is created from the latest main
- [ ] Branch is pushed to remote and available for subsequent tasks

## Test Requirements
- [ ] Verify branch TC-9005 exists on remote
- [ ] Verify branch point matches HEAD of main at time of creation

## Dependencies
None

[sdlc-workflow] Description digest: sha256-md:ee0b123c0f340a2d1157d020be0f0ad42f35fd497c843a91f9faf3e925e6e3ec

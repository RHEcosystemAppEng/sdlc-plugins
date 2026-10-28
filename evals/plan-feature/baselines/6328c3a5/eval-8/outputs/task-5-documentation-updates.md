## Repository
catalog-service

## Target Branch
main

## Description
Update documentation to reflect the addition of the `ownerGroup` field to Service Catalog records. The Feature's Documentation Considerations specify an "Updates" impact type: document that catalog records may be populated through registration, scheduled synchronization, fallback import, or on-demand refresh, and that all paths use the same catalog contract including the `ownerGroup` field.

Operators and API consumers need to understand that all population paths use the same catalog contract and that `ownerGroup` is part of the record schema.

## Acceptance Criteria
- [ ] Documentation accurately describes the `ownerGroup` field and its purpose
- [ ] Documentation lists all catalog population paths (registration, scheduled synchronization, fallback import, on-demand refresh) and notes they use the same catalog contract
- [ ] Documentation is consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify documentation accurately reflects the catalog record schema including `ownerGroup`
- [ ] Verify documentation describes all population paths and the shared catalog contract
- [ ] Verify documentation is complete and does not contradict the implementation

## Dependencies
- Depends on: Task 1 -- Add ownerGroup field to catalog record schema
- Depends on: Task 2 -- Populate ownerGroup during service registration
- Depends on: Task 3 -- Display ownerGroup in catalog summary API
- Depends on: Task 4 -- Display ownerGroup in downloadable report

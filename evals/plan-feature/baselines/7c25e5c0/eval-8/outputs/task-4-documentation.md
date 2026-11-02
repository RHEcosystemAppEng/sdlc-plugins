## Repository
catalog-service

## Target Branch
main

## Description
Document the `ownerGroup` field addition to the Service Catalog. Per the Documentation Considerations in TC-9007, this is an "Updates" doc impact: document that catalog records may be populated through registration, scheduled synchronization, fallback import, or on-demand refresh, and that all paths use the same catalog contract including the `ownerGroup` field.

Reference: Feature TC-9007.

## Acceptance Criteria
- [ ] Documentation accurately describes the `ownerGroup` field and its purpose
- [ ] Documentation lists all four population paths (registration, scheduled sync, fallback import, on-demand refresh) as documented in the Feature's Documentation Considerations
- [ ] Documentation explains the shared catalog contract

## Test Requirements
- [ ] Verify documentation is accurate and consistent with the implemented feature behavior
- [ ] Verify documentation covers the scope identified in Documentation Considerations

## Dependencies
- Depends on: Task 1 — Add ownerGroup to catalog store
- Depends on: Task 2 — Capture ownerGroup in registration
- Depends on: Task 3 — Display ownerGroup in consumers

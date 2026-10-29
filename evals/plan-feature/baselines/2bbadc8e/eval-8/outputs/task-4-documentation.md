## Repository
catalog-service

## Target Branch
main

## Description
Update documentation to reflect the addition of the `ownerGroup` field to Service Catalog records. The documentation should describe that catalog records may be populated through registration, scheduled synchronization, fallback import, or on-demand refresh, and that all paths use the same catalog contract. Operators and API consumers need to understand that `ownerGroup` is a new field on the catalog record and how it behaves across population paths.

Doc impact type: **Updates**

Reference: TC-9007

## Acceptance Criteria
- [ ] Documentation accurately describes the `ownerGroup` field and its purpose
- [ ] Documentation states that catalog records can be populated through multiple paths (registration, scheduled sync, fallback import, on-demand refresh)
- [ ] Documentation notes that all population paths use the same catalog contract
- [ ] Documentation covers the update-preserving semantics of `ownerGroup` (retained unless a new value is supplied)

## Test Requirements
- [ ] Verify documentation is accurate and consistent with the implemented feature behavior
- [ ] Verify documentation covers the scope identified in the Feature's Documentation Considerations section

## Dependencies
- Depends on: Task 1 — Add ownerGroup field to catalog record schema
- Depends on: Task 2 — Collect ownerGroup during registration
- Depends on: Task 3 — Display ownerGroup in summary API and report

## Repository
catalog-service

## Target Branch
main

## Description
Document the shared Service Catalog contract and the `ownerGroup` field. The documentation must explain that catalog records may be populated through four paths: registration, scheduled synchronization, fallback import, and on-demand refresh. All paths use the same catalog contract and produce records visible to the summary API and downloadable report. This is driven by the Feature's Documentation Considerations section (Doc Impact: Updates).

Reference: Feature TC-9007

## Acceptance Criteria
- [ ] Documentation explains the shared Service Catalog contract
- [ ] Documentation names registration, scheduled sync, fallback import, and on-demand refresh as population paths
- [ ] Documentation describes the `ownerGroup` field and its behavior across all population paths
- [ ] Documentation is consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify documentation accurately reflects the `ownerGroup` field semantics
- [ ] Verify all four population paths are named and described
- [ ] Verify documentation is consistent with the implemented feature behavior

## Dependencies
- Depends on: Task 2 — Update catalog writers
- Depends on: Task 3 — Update catalog consumers

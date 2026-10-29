## Repository
catalog-service

## Target Branch
main

## Description
Update documentation to reflect that Service Catalog records now include an `ownerGroup` field and may be populated through four distinct paths: registration, scheduled synchronization, fallback import, and on-demand refresh. The documentation should make clear that all population paths use the same shared Service Catalog contract, and that operators and API consumers need to understand this for proper integration.

Doc impact type: Updates to existing content.

Reference: Feature TC-9007 — Add an owner group to Service Catalog records.

## Acceptance Criteria
- [ ] Documentation accurately describes the `ownerGroup` field and its behavior
- [ ] Documentation explains the shared Service Catalog contract across all four population paths (registration, scheduled sync, fallback import, on-demand refresh)
- [ ] Documentation covers preservation semantics: existing `ownerGroup` is preserved when updates omit the field, and replaced when a new value is supplied
- [ ] Documentation reflects that the summary API and downloadable report display `ownerGroup` regardless of how the record was populated

## Test Requirements
- [ ] Verify documentation accurately reflects the implemented feature behavior
- [ ] Verify all four population paths (registration, scheduled sync, fallback import, on-demand refresh) are mentioned
- [ ] Verify the shared catalog contract is clearly explained for operators and API consumers

## Dependencies
- Depends on: Task 1 — Add `ownerGroup` field to Service Catalog records

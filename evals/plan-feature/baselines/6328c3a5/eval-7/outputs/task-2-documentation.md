## Repository
catalog-service

## Target Branch
main

## Description
Document the shared Service Catalog record contract changes for the `ownerGroup` field addition (Feature TC-9007). The documentation should explain that catalog records may be populated through four distinct paths (registration, scheduled synchronization, fallback import, and on-demand refresh) and that all paths use the same catalog contract with the `ownerGroup` field.

**Doc impact type:** Updates to existing content
**Details:** Document that catalog records may be populated through registration, scheduled synchronization, fallback import, or on-demand refresh. Operators and API consumers need to understand that all paths use the same catalog contract.

Reference: Feature TC-9007 — Add an owner group to Service Catalog records.

## Acceptance Criteria
- [ ] Documentation accurately reflects the `ownerGroup` field addition to Service Catalog records
- [ ] Documentation describes all four population paths (registration, scheduled sync, fallback import, on-demand refresh)
- [ ] Documentation explains the update-preservation semantics (existing `ownerGroup` preserved unless a new value is supplied)
- [ ] Documentation explains the shared catalog contract used across all population paths
- [ ] Content is accurate and consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify documentation accurately describes the `ownerGroup` field and its behavior across all population paths
- [ ] Verify documentation covers all four population paths without omitting any
- [ ] Verify documentation is consistent with the implementation in Task 1

## Dependencies
- Depends on: Task 1 — Add ownerGroup field to Service Catalog records

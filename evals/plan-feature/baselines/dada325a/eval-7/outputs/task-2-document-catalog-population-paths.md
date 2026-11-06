# Task 2 — Document Service Catalog population paths and the ownerGroup contract

**Summary:** TC-9007: Document catalog population paths and ownerGroup field
**Labels:** ai-generated-jira
**Priority:** Major (inherited from Feature)
**Fix Versions:** (omitted — Feature has none)
**Epic:** TC-9007: Service Catalog ownerGroup

## Repository
catalog-service

## Target Branch
main

## Description
Update the existing documentation for the Service Catalog to cover the `ownerGroup` field
added by TC-9007.

**Doc impact type:** Updates (to existing content).

The documentation must explain:
- Catalog records may be populated through four paths:
  - registration (initial onboarding)
  - scheduled synchronization
  - fallback import
  - on-demand refresh (`POST /api/catalog/refresh`)
- All four paths use the same catalog contract.
- Every record carries an `ownerGroup`. It is collected at onboarding and kept on later
  updates unless a new value is supplied.
- The summary API and the downloadable report show `ownerGroup`.
- `POST /api/catalog/refresh` accepts an optional `ownerGroup`.

**User purpose:** operators and API consumers need to understand that every population
path uses the same catalog contract, and where `ownerGroup` comes from.

Reference: Feature TC-9007, "Documentation Considerations".

## Acceptance Criteria
- [ ] The documentation lists all four population paths (registration, scheduled synchronization, fallback import, on-demand refresh) and states that they share one catalog contract
- [ ] The documentation describes the `ownerGroup` field: collected at onboarding, kept on update unless a new value is supplied, shown in the summary API and the downloadable report
- [ ] The documentation describes the optional `ownerGroup` input on `POST /api/catalog/refresh`

## Test Requirements
- [ ] Review the documentation against the merged Task 1 implementation and confirm that the described merge semantics and API fields match the actual behavior
- [ ] Confirm that every population path in the code is described and that no path is missing

## Dependencies
- Depends on: Task 1 — Add ownerGroup to the shared Service Catalog record across all writers and readers

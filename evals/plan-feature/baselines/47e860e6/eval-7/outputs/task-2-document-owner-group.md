# Task 2 — Document Service Catalog `ownerGroup` and record population paths

**Summary:** TC-9007: Document ownerGroup and catalog population paths
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**Fix Versions:** omitted (TC-9007 has none)

## Repository
catalog-service

## Target Branch
main

## Description
TC-9007 adds an `ownerGroup` field to Service Catalog records. The summary API and the downloadable report show it.

Doc impact type: **Updates to existing content**.

From the Feature's Documentation Considerations: document that catalog records may be populated through registration, scheduled synchronization, fallback import, or on-demand refresh. Operators and API consumers need to understand that all of these paths use the same catalog contract, including `ownerGroup`.

The docs must describe the `ownerGroup` behavior that was actually implemented on each population path. If the alternate paths (scheduled sync, fallback import, on-demand refresh) stay out of scope after the scope clarification on TC-9007, the docs must not claim that those paths populate or keep `ownerGroup`. Reference: TC-9007.

## Acceptance Criteria
- [ ] Documentation describes the `ownerGroup` field on Service Catalog records and where it appears (summary API, downloadable report)
- [ ] Documentation lists the four population paths: registration, scheduled synchronization, fallback import, on-demand refresh (`POST /api/catalog/refresh`)
- [ ] Documentation states the update rule: an existing `ownerGroup` is kept unless a new value is supplied, scoped to the paths where this is implemented
- [ ] Documentation does not claim behavior that was not implemented

## Test Requirements
- [ ] Review the documentation against the merged implementation for each population path and consumer, and confirm it is accurate and complete
- [ ] Confirm the field name, response shape, and report column match the implemented behavior

## Dependencies
- Depends on: Task 1 — Add `ownerGroup` to Service Catalog records for onboarding and display

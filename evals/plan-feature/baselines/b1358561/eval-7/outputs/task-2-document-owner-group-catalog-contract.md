# Task 2: Document the Service Catalog ownerGroup field and record population contract

**Labels**: ai-generated-jira
**Priority**: Major (inherited from TC-9007)
**fixVersions**: (none; the Feature has none)
**Parent / Links**: TC-9007 incorporates this task

## Repository
catalog-service

## Target Branch
main

## Description
Update the documentation for TC-9007 ("Add an owner group to Service Catalog records").

- **Doc impact type**: Updates to existing content.
- **What changed**: Service Catalog records gain an `ownerGroup` field. Registration collects it, and the catalog summary API and downloadable report display it.
- **Documentation Considerations from the Feature**: document that catalog records may be populated through registration, scheduled synchronization, fallback import, or on-demand refresh (`POST /api/catalog/refresh`). Operators and API consumers need to understand that all of these paths use the same catalog contract.

**Scope note:** TC-9007 has an open scope conflict. Task 1 implements `ownerGroup` only for registration and the display paths. Until the stakeholder decides whether scheduled sync, fallback import and on-demand refresh are in scope, the documentation must not claim that those paths populate or preserve `ownerGroup`. Document the guarantees that actually ship, and state any known limitation for records written by the other paths.

## Acceptance Criteria
- [ ] The documentation describes the `ownerGroup` field on Service Catalog records and shows where it appears (the summary API response and the downloadable report).
- [ ] The documentation lists the four population paths (registration, scheduled synchronization, fallback import, on-demand refresh) as writers of the same shared catalog contract.
- [ ] The documentation states the `ownerGroup` behavior that is implemented for each population path, with no unverified claims for paths that are still out of scope.
- [ ] The documentation describes the update rule: an existing `ownerGroup` is kept unless a new value is supplied, as implemented in Task 1.

## Test Requirements
- [ ] Review the documentation against the merged Task 1 implementation. Field name, response shape and report column must match the code.
- [ ] Confirm that every documented population path behavior matches the code as merged, and that limitations from the open scope decision are stated accurately.

## Dependencies
- Depends on: Task 1 — Add ownerGroup to Service Catalog records for registration, summary API, and report

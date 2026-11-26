# Task 4 — Document ownerGroup and the Service Catalog record contract

**Summary:** TC-9007: Document ownerGroup on Service Catalog records
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**Epic group (by-sub-feature):** Owner group display

## Repository
catalog-service

## Target Branch
main

## Description
Update the documentation to describe the new `ownerGroup` field on Service Catalog records (Feature TC-9007).

- **Doc impact type:** Updates to existing content
- **From the Documentation Considerations section:** document that catalog records may be populated through registration, scheduled synchronization, fallback import, or on-demand refresh, and that all of these paths use the same catalog contract. User purpose: operators and API consumers need to understand that every path uses the same catalog contract.

What changed in this Feature's planned scope:
- `ownerGroup` is collected during initial registration (onboarding).
- The catalog summary API and the downloadable report show `ownerGroup`.
- Store updates keep an existing `ownerGroup` when an update omits it and replace it when a new value is supplied.

**Scope caveat:** whether scheduled synchronization, fallback import, and on-demand refresh populate `ownerGroup` is unresolved pending stakeholder scope clarification (see the TC-9007 impact map). The documentation must describe the shared catalog contract and list all four population paths, but it must **not** state that every record has an `ownerGroup` regardless of population path unless that scope is approved and implemented. Until then, state that `ownerGroup` is set at registration and may be empty for records populated through other paths or created before this change.

## Acceptance Criteria
- [ ] Documentation describes the `ownerGroup` field, its meaning, and where it appears (summary API and downloadable report)
- [ ] Documentation describes the shared Service Catalog record contract and names all four population paths: registration, scheduled synchronization, fallback import, and on-demand refresh
- [ ] Documentation describes the update semantics: omitted keeps the existing value, supplied replaces it
- [ ] Documentation matches the scope actually delivered and makes no universal `ownerGroup` claim that is unresolved

## Test Requirements
- [ ] Review the documentation against the implemented behavior of Tasks 1–3 and confirm the field name, update semantics, and consumer output match
- [ ] Confirm that the population-path statements are accurate for the scope finally approved

## Dependencies
- Depends on: Task 1 — Add ownerGroup to the shared Service Catalog record schema and persistence
- Depends on: Task 2 — Collect and persist ownerGroup during initial registration
- Depends on: Task 3 — Display ownerGroup in the catalog summary API and downloadable report

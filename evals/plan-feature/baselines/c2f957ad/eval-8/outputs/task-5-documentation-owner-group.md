# Task 5 — Document the ownerGroup field on Service Catalog records

**Summary:** TC-9007: Document `ownerGroup` for catalog records, the summary API, and the report
**Issue type:** Task | **Parent Epic:** TC-9007: Owner group display and documentation
**Labels:** ai-generated-jira | **Priority:** Major | **Fix Versions:** (none — Feature has none)

## Repository
catalog-service

## Target Branch
main

## Description
Update the existing documentation for the new `ownerGroup` field on Service Catalog records, introduced by TC-9007.

- **Doc impact type:** Updates to existing content
- **What changed:** onboarding registration collects `ownerGroup` and requires it. Updates keep the stored owner group unless a new value is supplied. The catalog summary API returns `ownerGroup` per record (`null` when absent), and the downloadable report has an `ownerGroup` column (empty when absent).
- **From Documentation Considerations:** "document that catalog records may be populated through registration, scheduled synchronization, fallback import, or on-demand refresh". User purpose: operators and API consumers need to understand that all paths use the same catalog contract.
- **Scope caveat:** do **not** state that scheduled sync, fallback import, or on-demand refresh populate or preserve `ownerGroup`. Those paths are excluded from TC-9007 by stakeholder instruction and are an unresolved scope conflict in the impact map. You may document that these paths exist and write to the same catalog record. State that only registration is guaranteed to set `ownerGroup` until the scope question is resolved.
- Reference: Feature TC-9007.

## Acceptance Criteria
- [ ] Documentation describes the `ownerGroup` field, how it is collected at onboarding, and its preserve-on-update semantics
- [ ] Summary API documentation lists the `ownerGroup` response field and its `null` case
- [ ] Report documentation lists the `ownerGroup` column and its empty-cell case
- [ ] Documentation describes the catalog population paths without claiming `ownerGroup` behavior for the excluded paths

## Test Requirements
- [ ] Review the documentation against the merged behavior of Tasks 1–4 for accuracy and completeness
- [ ] Confirm no statement claims `ownerGroup` support for scheduled sync, fallback import, or on-demand refresh

## Dependencies
- Depends on: Task 1 — Add ownerGroup to the shared Service Catalog record schema
- Depends on: Task 2 — Collect ownerGroup during initial service registration
- Depends on: Task 3 — Show ownerGroup in the catalog summary API
- Depends on: Task 4 — Show ownerGroup in the downloadable catalog report

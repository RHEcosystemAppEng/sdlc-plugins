# Task 5 — Document the Service Catalog `ownerGroup` field

**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**Fix Versions:** (omitted — TC-9007 has no fixVersions)
**Parent / Epic:** TC-9007: Documentation (if Epic type available)

## Repository
catalog-service

## Target Branch
main

## Description
Document the new `ownerGroup` field on Service Catalog records for operators and API consumers (TC-9007).

- **Doc impact type:** Updates to existing content
- **What changed:** Service Catalog records gain an `ownerGroup` field that is collected during initial registration, preserved on update unless a new value is supplied, and displayed in the catalog summary API response and the downloadable report.
- **User purpose (from Documentation Considerations):** operators and API consumers need to understand the catalog contract for `ownerGroup`.
- **Scope caveat:** the Documentation Considerations ask to state that records may be populated through registration, scheduled synchronization, fallback import, or on-demand refresh and that "all paths use the same catalog contract". Under the current stakeholder-limited scope, only registration is updated to populate `ownerGroup`; the other population paths are UNRESOLVED in the TC-9007 impact map. Do **not** document that every population path sets or preserves `ownerGroup` unless the scope conflict on TC-9007 has been resolved and those paths have been updated. Document legacy/missing `ownerGroup` behavior as implemented (sentinel value).
- Reference: TC-9007.

## Acceptance Criteria
- [ ] Documentation describes the `ownerGroup` field, its meaning, and that it is required at registration
- [ ] Documentation describes preserve-on-update semantics (current value kept unless a new value is supplied)
- [ ] Summary API documentation lists the `ownerGroup` response field and its missing-value representation
- [ ] Downloadable report documentation lists the `ownerGroup` column
- [ ] Documentation does not claim that all population paths set `ownerGroup` unless the TC-9007 scope conflict has been resolved and implemented

## Test Requirements
- [ ] Verify documented field names, types, and missing-value representation match the behavior implemented in Tasks 1–4
- [ ] Verify documentation statements about population paths are consistent with the resolved TC-9007 scope

## Dependencies
- Depends on: Task 1 — Add `ownerGroup` to the shared Service Catalog record schema with preserve-on-update semantics
- Depends on: Task 2 — Collect `ownerGroup` during initial service registration
- Depends on: Task 3 — Show `ownerGroup` in the catalog summary API
- Depends on: Task 4 — Show `ownerGroup` in the downloadable catalog report

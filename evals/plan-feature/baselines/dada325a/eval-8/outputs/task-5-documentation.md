# Task 5 — Document the ownerGroup field on Service Catalog records

**Summary:** TC-9007: Document `ownerGroup` on Service Catalog records
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**Epic group (by-sub-feature, pending approval):** TC-9007: Owner group display

## Repository
catalog-service

## Target Branch
main

## Description
Document the new `ownerGroup` field added by TC-9007.

- **What changed:** Service Catalog records now carry an `ownerGroup` collected during initial registration; updates preserve the current owner group unless a new value is supplied; the catalog summary API and the downloadable report display `ownerGroup`.
- **Doc impact type:** Updates (to existing content).
- **Documentation Considerations (from TC-9007):** document that catalog records may be populated through registration, scheduled synchronization, fallback import, or on-demand refresh, and that all paths use the same catalog contract. **User purpose:** operators and API consumers need to understand that all paths use the same catalog contract.
- **Scope caveat:** the TC-9007 impact map records an unresolved scope conflict — scheduled synchronization, fallback import, and on-demand refresh were excluded by the stakeholder. Do not document that those paths populate or preserve `ownerGroup` unless the scope conflict is resolved and those paths are implemented and tested; until then, document the field for registration and the summary/report display, and describe the other paths only as existing population paths without `ownerGroup` guarantees.
- **Reference:** Feature TC-9007.

## Acceptance Criteria
- [ ] Documentation describes the `ownerGroup` field, how it is set at registration, and its preserve-on-update semantics
- [ ] Documentation shows `ownerGroup` in the summary API response and downloadable report
- [ ] Documentation accurately reflects which population paths are guaranteed to set/preserve `ownerGroup`, consistent with the resolved scope

## Test Requirements
- [ ] Verify the documented field name, behavior, and outputs match the implemented behavior from Tasks 1–4
- [ ] Verify no documented claim covers population paths that were not implemented and tested

## Dependencies
- Depends on: Task 1 — Add ownerGroup to the shared Service Catalog record schema
- Depends on: Task 2 — Collect ownerGroup during service registration
- Depends on: Task 3 — Show ownerGroup in the catalog summary API
- Depends on: Task 4 — Show ownerGroup in the downloadable catalog report

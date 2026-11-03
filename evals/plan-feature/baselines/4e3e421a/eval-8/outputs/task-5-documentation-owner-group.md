# Task 5 — Document the `ownerGroup` Service Catalog field

**Labels**: ai-generated-jira
**Priority**: Major (inherited from TC-9007)
**Fix Versions**: (omitted — TC-9007 has no fixVersions)

## Repository
catalog-service

## Target Branch
main

## Description
Update the documentation for TC-9007 ("Add an owner group to Service Catalog records").

- **Doc impact type:** Updates to existing content.
- **What changed:** Service Catalog records now carry an `ownerGroup`. It is collected during initial registration, kept on updates unless a new value is supplied, and shown in the catalog summary API and the downloadable report.
- **User purpose (from Documentation Considerations):** operators and API consumers need to understand that the catalog record contract, including `ownerGroup`, is shared.
- **Scope note:** The Documentation Considerations ask for docs on every population path: registration, scheduled synchronization, fallback import, and on-demand refresh. The stakeholder limited the implementation to onboarding and display, and coverage of the other paths is an open question in the TC-9007 impact map. Document the registration and display behavior now. Add `ownerGroup` behavior for the other paths only after that scope question is resolved, and do not describe it as implemented before then.

## Acceptance Criteria
- [ ] The documentation describes the `ownerGroup` field on Service Catalog records and how it is collected during registration
- [ ] The documentation describes the preserve-on-update semantics
- [ ] The documentation lists `ownerGroup` in the summary API response and the downloadable report
- [ ] The documentation does not claim `ownerGroup` coverage for population paths that were not implemented

## Test Requirements
- [ ] Check that the documented field name, registration input, update semantics, and API/report output match the behavior implemented in Tasks 1–4
- [ ] Check that the documentation is consistent with the resolved TC-9007 scope

## Dependencies
- Depends on: Task 1 — Add `ownerGroup` to the Service Catalog record schema and persistence helpers
- Depends on: Task 2 — Collect `ownerGroup` during service registration
- Depends on: Task 3 — Show `ownerGroup` in the catalog summary API
- Depends on: Task 4 — Show `ownerGroup` in the downloadable catalog report

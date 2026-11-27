# Task 5 — Document ownerGroup in the Service Catalog record contract

**Summary:** TC-9007: Document the ownerGroup field in the Service Catalog contract
**Epic:** TC-9007: Owner group display
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**fixVersions:** omitted (Feature has none)

## Repository
catalog-service

## Target Branch
main

## Description
Update the documentation for the `ownerGroup` field added by TC-9007.

- **Doc impact type:** Updates to existing content.
- **What changed:** Service Catalog records gain an `ownerGroup` field. It is collected during initial registration, kept on updates that omit it, and replaced when an update supplies a new value. The catalog summary API and the downloadable report show it, with `null` or empty values for records stored without one.
- **User purpose (from Documentation Considerations):** operators and API consumers need to understand the shared catalog contract.
- **Scope caveat:** the Documentation Considerations also ask for a statement that records may be populated through scheduled synchronization, fallback import or on-demand refresh, and that all paths use the same catalog contract. Under the current stakeholder scope those paths are not changed or validated. Do not document that they set or preserve `ownerGroup` until the scope conflict recorded in the TC-9007 impact map is resolved. Document only the behavior the implementation tasks verify.
- **Reference:** Feature TC-9007.

## Acceptance Criteria
- [ ] The documentation describes the `ownerGroup` field, how it is collected during registration, and the update semantics (omitted means kept, supplied means replaced).
- [ ] The documentation describes `ownerGroup` in the summary API response and in the downloadable report, including how records without a value are represented.
- [ ] The documentation makes no claims about `ownerGroup` behavior for population paths that are not covered by implemented and tested tasks.

## Test Requirements
- [ ] Review the documentation against the merged implementation of Tasks 1–4 for accuracy (field name, update semantics, null/empty representation).
- [ ] Confirm the documentation is consistent with the summary API response and report output produced by the tests in Tasks 3 and 4.

## Dependencies
- Depends on: Task 1 — Add ownerGroup to the shared Service Catalog record schema
- Depends on: Task 2 — Collect ownerGroup during initial service registration
- Depends on: Task 3 — Expose ownerGroup in the catalog summary API
- Depends on: Task 4 — Include ownerGroup in the downloadable catalog report

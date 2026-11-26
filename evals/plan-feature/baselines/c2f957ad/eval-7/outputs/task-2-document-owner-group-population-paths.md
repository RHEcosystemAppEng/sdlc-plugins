# Task 2 — Document ownerGroup and the shared catalog population paths

- **Issue type:** Task
- **Parent (Epic):** TC-9007: Service Catalog ownerGroup
- **Labels:** ai-generated-jira
- **Priority:** Major (inherited from TC-9007)
- **Fix Versions:** omitted (TC-9007 has none)
- **Links:** depends on Task 1

---

## Repository
catalog-service

## Target Branch
main

## Description
Update the catalog-service documentation for the `ownerGroup` field added by TC-9007.

- **Doc impact type:** Updates to existing content.
- **What changed:** Service Catalog records now carry an `ownerGroup` value. The catalog summary API and the downloadable report show it. When a record is updated, the current owner group is kept unless a new value is supplied.
- **Details from Documentation Considerations:** state that catalog records may be populated through **registration**, **scheduled synchronization**, **fallback import**, or **on-demand refresh** (`POST /api/catalog/refresh`). All four paths use the same catalog record contract, including `ownerGroup`.
- **Audience / user purpose:** operators and API consumers need to understand that every population path uses the same catalog contract.
- Feature reference: TC-9007.

## Acceptance Criteria
- [ ] The documentation describes the `ownerGroup` field, where it appears (summary API and downloadable report), and its preserve-unless-supplied update rule.
- [ ] The documentation lists all four population paths (registration, scheduled synchronization, fallback import, on-demand refresh) and states that they share the same catalog contract.
- [ ] The documentation for `POST /api/catalog/refresh` covers the optional `ownerGroup` input.
- [ ] The documentation covers the fail-closed behavior: a record is not persisted without an `ownerGroup`.

## Test Requirements
- [ ] Check every documented behavior against the merged Task 1 implementation and tests: field name, update rule, fail-closed behavior, and each population path.
- [ ] Confirm that no population path described in the code is missing from the docs, and that the docs describe no path that does not exist.

## Dependencies
- Depends on: Task 1 — Add ownerGroup to Service Catalog records across all population paths and displays

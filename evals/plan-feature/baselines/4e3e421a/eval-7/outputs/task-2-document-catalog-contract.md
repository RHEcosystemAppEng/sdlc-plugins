# Task 2 — Document the shared catalog contract and ownerGroup across population paths

**Summary:** TC-9007: Document ownerGroup and the shared Service Catalog population contract
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**Fix Versions:** (omitted — Feature has none)

## Repository
catalog-service

## Target Branch
main

## Description
TC-9007 adds an `ownerGroup` field to Service Catalog records and shows it in the catalog summary API and the downloadable report. This task updates the existing documentation to match.

**Doc impact type:** Updates to existing content.

What the documentation must say, from TC-9007's Documentation Considerations:

- Catalog records can be populated through four paths: initial registration, scheduled synchronization, fallback import, and on-demand refresh (`POST /api/catalog/refresh`).
- All four paths use the same catalog contract, including `ownerGroup`.

**User purpose.** Operators and API consumers need to know that every path uses the same catalog contract.

Also cover:

- `ownerGroup` is collected at registration.
- `ownerGroup` is kept on updates unless a new value is supplied, for example through the optional `ownerGroup` on `POST /api/catalog/refresh`.
- `ownerGroup` appears in the summary API response and the downloadable report.

Reference: TC-9007.

## Acceptance Criteria
- [ ] The documentation lists all four population paths (registration, scheduled synchronization, fallback import, on-demand refresh) and states that they share one catalog record contract.
- [ ] The documentation describes `ownerGroup`: it is collected at registration, kept on updates unless a new value is supplied, and shown in the summary API and the downloadable report.
- [ ] The documentation describes the optional `ownerGroup` on `POST /api/catalog/refresh` and what happens when it is omitted.
- [ ] The documentation matches the behavior implemented in Task 1.

## Test Requirements
- [ ] Check the documented population paths and `ownerGroup` behavior against the merged Task 1 implementation and its tests.
- [ ] Check that the summary API and report field names in the docs match the actual response and export output.
- [ ] Check that the docs are complete: no population path or `ownerGroup` rule from TC-9007 is missing.

## Dependencies
- Depends on: Task 1 — Add ownerGroup to Service Catalog records across all population paths and readers

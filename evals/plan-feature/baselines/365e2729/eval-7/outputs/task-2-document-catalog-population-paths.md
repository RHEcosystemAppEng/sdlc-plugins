# Task 2 — Document Service Catalog population paths and the `ownerGroup` contract

**Summary:** TC-9007: Document catalog population paths and ownerGroup contract
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**Fix Versions:** omitted (TC-9007 has none)

## Repository
catalog-service

## Target Branch
main

## Description
Update the existing documentation to reflect TC-9007 (add an owner group to Service Catalog records).

**Doc impact type:** Updates to existing content.

**What changed:** Service Catalog records now carry an `ownerGroup` field. The catalog summary API and the downloadable report display it. Records can be populated through four paths: initial registration (onboarding), scheduled provider sync, fallback import of previously exported data, and the on-demand `POST /api/catalog/refresh` API. All four use the same catalog record contract. `ownerGroup` is set at creation and kept on update unless a new value is supplied.

**User purpose (from Documentation Considerations):** operators and API consumers need to understand that all population paths use the same catalog contract.

Feature: TC-9007.

## Acceptance Criteria
- [ ] The documentation lists all four population paths (registration, scheduled sync, fallback import, on-demand refresh) and states that they share one catalog record contract.
- [ ] The documentation describes the `ownerGroup` field, where it appears (summary API, downloadable report), and its preserve-unless-supplied update rule.
- [ ] The documentation describes the optional `ownerGroup` parameter on `POST /api/catalog/refresh` and the behavior when no `ownerGroup` is available (as implemented in Task 1).

## Test Requirements
- [ ] Check the documented field names, endpoint path and update semantics against the merged Task 1 implementation.
- [ ] Confirm the docs cover every population path named in the Documentation Considerations and contradict nothing in the summary API or report output.

## Dependencies
- Depends on: Task 1 — Add `ownerGroup` to Service Catalog records across all population paths and readers

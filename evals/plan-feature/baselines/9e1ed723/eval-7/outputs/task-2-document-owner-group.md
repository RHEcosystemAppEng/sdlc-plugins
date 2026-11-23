# Task 2 — Document ownerGroup and Service Catalog population paths

**Summary:** TC-9007: Document ownerGroup and Service Catalog population paths
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**Fix Versions:** (omitted — TC-9007 has none)
**Parent:** Epic "TC-9007: Owner group on Service Catalog records" if a level-1 type is discovered; otherwise none (Feature "Incorporates" link)

## Repository
catalog-service

## Target Branch
main

## Description
Update the catalog-service documentation for TC-9007 (Add an owner group to Service Catalog records).

- **What changed:** Service Catalog records gain an `ownerGroup` field, collected during initial onboarding/registration and shown by the catalog summary API and the downloadable report. Updates preserve the current owner group unless a new value is supplied.
- **Doc impact type:** Updates to existing content.
- **Details (from Documentation Considerations):** document that catalog records may be populated through registration, scheduled synchronization, fallback import, or on-demand refresh (`POST /api/catalog/refresh`). User purpose: operators and API consumers need to understand that all paths use the same catalog contract.
- **Caveat:** whether scheduled sync, fallback import, and on-demand refresh set/preserve `ownerGroup` is an unresolved scope conflict on TC-9007. The documentation must describe only the behavior actually implemented when this task is picked up — do not state that all population paths guarantee `ownerGroup` unless the expanded-scope work has been approved and merged.

## Acceptance Criteria
- [ ] Documentation describes the `ownerGroup` field, how it is supplied at registration, and that updates preserve it unless a new value is supplied
- [ ] Documentation shows `ownerGroup` in the summary API response and the downloadable report
- [ ] Documentation lists all four population paths (registration, scheduled synchronization, fallback import, on-demand refresh) and accurately states the `ownerGroup` behavior of each as implemented
- [ ] Documentation is consistent with the merged implementation of TC-9007

## Test Requirements
- [ ] Review the documentation against the merged code and tests for accuracy of field name, API response shape, and report column
- [ ] Verify each population path's described `ownerGroup` behavior matches the implementation (no unimplemented guarantees)

## Dependencies
- Depends on: Task 1 — Add ownerGroup to Service Catalog records for onboarding, summary API, and report
- Depends on: any additional writer task approved through the TC-9007 scope decision

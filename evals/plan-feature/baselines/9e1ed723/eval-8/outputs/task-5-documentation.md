# Task 5 — Document the Service Catalog ownerGroup field

**Summary:** TC-9007: Document the ownerGroup field on Service Catalog records
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**Fix Versions:** (none; the Feature has no fixVersions)
**Epic group (by-sub-feature, pending approval):** Documentation

## Repository
catalog-service

## Target Branch
main

## Description
Update the existing documentation for TC-9007 ("Add an owner group to Service Catalog records").

- **What changed:** Service Catalog records now carry an `ownerGroup` field. It is collected during initial onboarding and shown in the catalog summary API and the downloadable report. Updates keep the current owner group unless a new value is supplied.
- **Doc impact type:** Updates to existing content.
- **Details from Documentation Considerations:** document that catalog records may be populated through registration, scheduled synchronization, fallback import, or on-demand refresh, and that all paths use the same catalog contract. Audience: operators and API consumers.
- **Scope caveat:** the TC-9007 impact map has an unresolved scope conflict. Only the onboarding writer and the display consumers are in scope for implementation. Before stating that every population path sets or preserves `ownerGroup`, confirm how that conflict was resolved. If the other paths stay out of scope, document `ownerGroup` as set at onboarding and note that records populated by other paths may not have it.

## Acceptance Criteria
- [ ] Documentation describes the `ownerGroup` field, how it is set during onboarding, and how updates preserve it
- [ ] Documentation describes `ownerGroup` in the summary API response and the downloadable report
- [ ] Documentation states which population paths set `ownerGroup`, and the statement matches the implemented and approved scope
- [ ] Documentation explains to operators and API consumers that all population paths share the same catalog record contract

## Test Requirements
- [ ] Review the documentation against the merged implementation (Tasks 1–4) and confirm field name, null/empty handling, and update semantics match
- [ ] Confirm no documentation claims behavior for population paths that were not implemented

## Dependencies
- Depends on: Task 1 — Add ownerGroup to the shared Service Catalog record schema
- Depends on: Task 2 — Collect ownerGroup during service onboarding
- Depends on: Task 3 — Show ownerGroup in the catalog summary API
- Depends on: Task 4 — Include ownerGroup in the downloadable catalog report

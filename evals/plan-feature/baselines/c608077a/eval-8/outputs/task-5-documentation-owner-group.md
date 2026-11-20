# Task 5 — Document the ownerGroup catalog contract

**Epic:** TC-9007: Owner group display
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)

## Repository
catalog-service

## Target Branch
main

## Description
Documentation task for TC-9007 (doc impact: **Updates to existing content**).

What changed: Service Catalog records gain an `ownerGroup` field. It is collected during initial registration, kept on updates unless a new value is supplied, and shown in the catalog summary API and the downloadable report.

Documentation Considerations from the Feature: "document that catalog records may be populated through registration, scheduled synchronization, fallback import, or on-demand refresh", so that operators and API consumers understand that all paths use the same catalog contract.

Important scope caveat: in the current plan only the registration path is updated to supply `ownerGroup`. The scheduled-sync, fallback-import, and on-demand-refresh writers are excluded by stakeholder instruction and recorded as unresolved in the TC-9007 impact map. The documentation must describe the contract accurately for what is actually implemented. It must not say that all population paths set `ownerGroup` unless the scope conflict is resolved and those paths are implemented. Until then, document that `ownerGroup` may be `null`/empty for records populated through paths other than registration.

## Acceptance Criteria
- [ ] Documentation describes the `ownerGroup` field, how it is supplied at registration, and its update-preservation semantics
- [ ] Documentation describes `ownerGroup` in the summary API response and the downloadable report, including `null`/empty semantics
- [ ] Documentation lists the population paths (registration, scheduled synchronization, fallback import, on-demand refresh) and accurately states which of them populate `ownerGroup` as implemented

## Test Requirements
- [ ] Review the documentation against the merged implementation of Tasks 1–4. Field names, API shape, report column, and null semantics must match.
- [ ] Confirm the documentation does not claim `ownerGroup` coverage for population paths that were not implemented

## Dependencies
- Depends on: Task 1 — Add ownerGroup to the shared Service Catalog record schema
- Depends on: Task 2 — Collect ownerGroup during initial service registration
- Depends on: Task 3 — Show ownerGroup in the catalog summary API
- Depends on: Task 4 — Include ownerGroup in the downloadable catalog report

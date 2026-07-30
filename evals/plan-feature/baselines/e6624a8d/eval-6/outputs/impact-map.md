# Repository Impact Map

**Feature:** TC-9006 — Add vulnerability remediation tracking dashboard
**Priority:** Major
**Fix Versions:** RHTPA 1.5.0

## Epic Hierarchy

This feature uses **Feature -> Epic -> Task** hierarchy with **by-repository** grouping.

Issue type mapping:
- Feature: TC-9006 (level 2)
- Epic: level-1 issue type named 'Epic'
- Task: level-0 issue type

### Epic Plan

| Epic | Summary | Repository | Tasks |
|---|---|---|---|
| Epic A | TC-9006: trustify-backend | trustify-backend | Tasks 1, 2, 3, 8 |
| Epic B | TC-9006: trustify-ui | trustify-ui | Tasks 4, 5, 6, 7 |

**Epic creation details:**
- Issue type: Epic (hierarchyLevel 1)
- Parent: TC-9006 (the Feature issue)
- Labels: ["ai-generated-jira"]
- Priority: Major (inherited from Feature)
- Fix Versions: RHTPA 1.5.0 (inherited from Feature)

**Incorporates links:** Feature TC-9006 links to each Epic (not to individual Tasks).

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators identified. The backend and frontend changes reside in separate repositories (trustify-backend and trustify-ui). Backend tasks can be merged to main independently and deployed before frontend work begins. No coordinated schema migrations, no breaking API changes (the endpoints are new), no cross-cutting refactors. Task ordering via dependencies ensures backend endpoints exist before frontend consumption begins.

## Impact Map

```
trustify-backend:
  changes:
    - Add remediation model structs (RemediationSummary, ProductRemediation) in a new remediation module
    - Add remediation aggregation service that computes counts from existing vulnerability and SBOM relationship data
    - Add GET /api/v2/remediation/summary endpoint returning aggregated counts by severity and status
    - Add GET /api/v2/remediation/by-product endpoint returning per-product remediation breakdown
    - Add integration tests for both remediation endpoints
    - Document remediation API endpoints and dashboard usage

trustify-ui:
  changes:
    - Add TypeScript interfaces for remediation API response types
    - Add API client functions for remediation endpoints
    - Add React Query hooks for remediation data fetching
    - Create RemediationDashboardPage with summary cards and progress chart
    - Add route definition for /remediation path
    - Add filterable vulnerability table component with severity, product, and status filters
    - Add unit tests (Vitest + RTL) and E2E tests (Playwright) for the remediation dashboard
    - Add MSW mock handlers and fixture data for remediation endpoints
```

## Excluded Requirements

- **Export remediation report as CSV** (Requirement from Feature, marked non-MVP) — Deferred to post-MVP iteration. This requirement is fully specifiable but excluded from the current plan per its non-MVP designation. Will be planned in a subsequent iteration after the MVP dashboard is delivered and validated.

## Documentation Signals

- **Doc impact type:** New Content
- **Details:** Document the remediation dashboard and aggregation endpoints. Security teams need a guide for using the dashboard; API consumers need endpoint reference.

## Task Summary

| # | Summary | Repository | Epic | Dependencies |
|---|---|---|---|---|
| 1 | Add remediation model and aggregation service | trustify-backend | TC-9006: trustify-backend | None |
| 2 | Add remediation summary and by-product API endpoints | trustify-backend | TC-9006: trustify-backend | Task 1 |
| 3 | Add integration tests for remediation endpoints | trustify-backend | TC-9006: trustify-backend | Task 2 |
| 4 | Add remediation API types, client functions, and hooks | trustify-ui | TC-9006: trustify-ui | Task 2 |
| 5 | Create Remediation Dashboard page with summary cards and progress chart | trustify-ui | TC-9006: trustify-ui | Task 4 |
| 6 | Add filterable vulnerability table to remediation dashboard | trustify-ui | TC-9006: trustify-ui | Task 5 |
| 7 | Add tests for remediation dashboard | trustify-ui | TC-9006: trustify-ui | Tasks 5, 6 |
| 8 | Document remediation dashboard and API endpoints | trustify-backend | TC-9006: trustify-backend | Tasks 1, 2, 3, 4, 5, 6, 7 |

# Repository Impact Map — TC-9006

## Feature: Add vulnerability remediation tracking dashboard

**Priority**: Major (inherited — propagated to all tasks)
**Fix Versions**: RHTPA 1.5.0 (inherited — propagated to all tasks, fixVersion scope defaults to "both")

## Workflow Mode

**Selected mode**: `direct-to-main`
**Rationale**: No atomicity indicators identified. The backend endpoints can be merged independently and the frontend can be developed against them once available. No coordinated schema migrations, no breaking API changes to existing endpoints (new endpoints only), no cross-cutting refactors.

## Epic Grouping

**Strategy**: `by-repository` (from CLAUDE.md Hierarchy Configuration)
**Level-1 issue type**: Epic (hierarchyLevel 1)

### Epic 1: TC-9006: trustify-backend

- **Issue type**: Epic (level 1)
- **Parent**: TC-9006
- **Summary**: TC-9006: trustify-backend
- **Description**: Backend aggregation endpoints for vulnerability remediation tracking — summary by severity/status and breakdown by product.
- **Labels**: ["ai-generated-jira"]
- **Priority**: Major (inherited from Feature)
- **Fix Versions**: RHTPA 1.5.0 (inherited from Feature)
- **Tasks**: Task 1, Task 2, Task 3, Task 4

### Epic 2: TC-9006: trustify-ui

- **Issue type**: Epic (level 1)
- **Parent**: TC-9006
- **Summary**: TC-9006: trustify-ui
- **Description**: Frontend remediation tracking dashboard with summary cards, progress chart, and filterable vulnerability table.
- **Labels**: ["ai-generated-jira"]
- **Priority**: Major (inherited from Feature)
- **Fix Versions**: RHTPA 1.5.0 (inherited from Feature)
- **Tasks**: Task 5, Task 6, Task 7, Task 8

## Issue Links

- **Incorporates**: TC-9006 → Epic 1 (TC-9006: trustify-backend)
- **Incorporates**: TC-9006 → Epic 2 (TC-9006: trustify-ui)

Note: Incorporates links go from the Feature to each Epic, not from the Feature to individual Tasks. Tasks inherit hierarchy through their Epic parent.

## Changes

trustify-backend:
  changes:
    - Add remediation summary model with aggregation types (severity × status matrix)
    - Add RemediationService with summary and by-product aggregation queries
    - Add GET /api/v2/remediation/summary endpoint returning counts by severity and status
    - Add GET /api/v2/remediation/by-product endpoint returning per-product remediation breakdown
    - Add integration tests for both remediation endpoints

trustify-ui:
  changes:
    - Add TypeScript interfaces for remediation API response types
    - Add API client functions for remediation endpoints
    - Add React Query hooks for remediation data fetching
    - Add RemediationDashboardPage with summary cards, progress chart, and filterable vulnerability table
    - Add route registration for /remediation path
    - Add MSW handlers and component tests for the dashboard

## Excluded Requirements

- **Export remediation report as CSV**: Non-MVP requirement. Can be planned in a follow-up feature once the dashboard and endpoints are established.

## Documentation Signals

- **Doc Impact**: New Content
- **Details**: Security teams need a guide for using the dashboard; API consumers need endpoint reference
- A documentation task will be generated (Task 9).

## Inherited Field Propagation Summary

| Field | Feature Value | Propagated to Tasks | Propagated to Epics | Rationale |
|---|---|---|---|---|
| Priority | Major | Yes | Yes | Feature priority is set (not "Undefined") |
| Fix Versions | RHTPA 1.5.0 | Yes | Yes | Feature has fixVersions; fixVersion scope defaults to "both" |

## Task Summary

| # | Task | Repository | Epic | Dependencies |
|---|---|---|---|---|
| 1 | Remediation summary model and service | trustify-backend | TC-9006: trustify-backend | None |
| 2 | Remediation summary endpoint | trustify-backend | TC-9006: trustify-backend | Task 1 |
| 3 | Remediation by-product endpoint | trustify-backend | TC-9006: trustify-backend | Task 1 |
| 4 | Backend integration tests | trustify-backend | TC-9006: trustify-backend | Task 2, Task 3 |
| 5 | Frontend API types and client functions | trustify-ui | TC-9006: trustify-ui | Task 2, Task 3 |
| 6 | React Query hooks for remediation data | trustify-ui | TC-9006: trustify-ui | Task 5 |
| 7 | Remediation dashboard page | trustify-ui | TC-9006: trustify-ui | Task 6 |
| 8 | Frontend tests | trustify-ui | TC-9006: trustify-ui | Task 7 |
| 9 | Documentation | trustify-backend | TC-9006: trustify-backend | Task 4, Task 8 |

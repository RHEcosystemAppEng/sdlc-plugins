# Repository Impact Map — TC-9006

## Feature

**TC-9006**: Add vulnerability remediation tracking dashboard

## Workflow Mode

**direct-to-main** — The backend and frontend reside in separate repositories. Each task produces an independent PR that can be merged to `main` without breaking the other repository. The frontend can be developed with MSW mocks while backend endpoints are in progress. No atomicity indicators (coordinated schema migrations, breaking API changes, cross-cutting refactors, or tightly coupled same-repo components) are present.

## Epic Hierarchy

Grouping strategy: **by-repository** (from CLAUDE.md Hierarchy Configuration)

### Epic 1: TC-9006: trustify-backend

- **Issue type**: Epic (level 1)
- **Parent**: TC-9006 (Feature)
- **Description**: Backend remediation aggregation module — new REST endpoints for vulnerability remediation summary by severity/status and per-product breakdown, computed from existing SBOM-advisory relationship data.
- **Tasks**: Task 1, Task 2, Task 3

### Epic 2: TC-9006: trustify-ui

- **Issue type**: Epic (level 1)
- **Parent**: TC-9006 (Feature)
- **Description**: Frontend remediation dashboard — new page at /remediation with summary cards, progress chart, filterable vulnerability table, and supporting API client layer with React Query hooks.
- **Tasks**: Task 4, Task 5, Task 6, Task 7

## Incorporates Links

- TC-9006 **incorporates** Epic "TC-9006: trustify-backend"
- TC-9006 **incorporates** Epic "TC-9006: trustify-ui"

(Links go from Feature to Epics, not from Feature to individual Tasks.)

## Impact Map

```
trustify-backend:
  changes:
    - Create remediation module (model/service/endpoints) following existing domain module pattern
    - Add GET /api/v2/remediation/summary endpoint returning aggregated counts by severity and status
    - Add GET /api/v2/remediation/by-product endpoint returning per-product remediation breakdown
    - Add integration tests for both remediation endpoints

trustify-ui:
  changes:
    - Add TypeScript interfaces for remediation API response types
    - Add API client functions for remediation endpoints
    - Add React Query hooks for remediation data fetching
    - Create RemediationDashboardPage with summary cards and progress chart
    - Add filterable vulnerability table component to the dashboard
    - Add route definition for /remediation and navigation entry
    - Add unit tests (Vitest + RTL), MSW mock handlers, and E2E test (Playwright)
```

## Task Summary

| # | Summary | Repository | Parent Epic |
|---|---|---|---|
| 1 | Create remediation module with summary aggregation endpoint | trustify-backend | TC-9006: trustify-backend |
| 2 | Add per-product remediation breakdown endpoint | trustify-backend | TC-9006: trustify-backend |
| 3 | Add integration tests for remediation endpoints | trustify-backend | TC-9006: trustify-backend |
| 4 | Add remediation API types, client functions, and React Query hooks | trustify-ui | TC-9006: trustify-ui |
| 5 | Create remediation dashboard page with summary cards and progress chart | trustify-ui | TC-9006: trustify-ui |
| 6 | Add filterable vulnerability table to remediation dashboard | trustify-ui | TC-9006: trustify-ui |
| 7 | Add remediation dashboard unit and E2E tests | trustify-ui | TC-9006: trustify-ui |

## Inherited Fields

- **Priority**: Major (propagated to all tasks and Epics)
- **Fix Versions**: RHTPA 1.5.0 (propagated to all tasks and Epics; fixVersion scope defaults to "both")

## additional_fields (per task and Epic)

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

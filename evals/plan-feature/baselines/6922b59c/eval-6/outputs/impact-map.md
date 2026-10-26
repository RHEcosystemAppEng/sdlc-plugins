# Repository Impact Map — TC-9006

## Feature Summary

Add vulnerability remediation tracking dashboard with backend aggregation endpoints
and a frontend dashboard page showing summary cards, progress chart, and filterable
vulnerability table.

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. The backend endpoints are entirely
new (they do not modify existing API contracts) and can be merged independently. The
frontend dashboard is a new page at `/remediation` that does not modify existing UI
pages. Backend tasks can be delivered first, followed by frontend tasks, without
leaving `main` in a broken state at any point. No coordinated schema migrations,
no breaking API changes, no cross-cutting refactors, and no tightly coupled components
that require all-or-nothing delivery.

## Epic Hierarchy

Grouping strategy: **by-repository** (from CLAUDE.md Hierarchy Configuration)

### Epic 1: TC-9006: trustify-backend

- **Issue type:** Epic (level-1)
- **Parent:** TC-9006 (Feature)
- **Summary:** TC-9006: trustify-backend
- **Description:** Backend implementation for the vulnerability remediation tracking
  dashboard. Adds remediation model structs, aggregation service, REST endpoints
  (summary and by-product), and integration tests.
- **additional_fields:**
  - `labels`: ["ai-generated-jira"]
  - `priority`: {"name": "Major"}
  - `fixVersions`: [{"name": "RHTPA 1.5.0"}]
- **Tasks:** Task 1, Task 2, Task 3

### Epic 2: TC-9006: trustify-ui

- **Issue type:** Epic (level-1)
- **Parent:** TC-9006 (Feature)
- **Summary:** TC-9006: trustify-ui
- **Description:** Frontend implementation for the vulnerability remediation tracking
  dashboard. Adds API types, client functions, React Query hooks, dashboard page with
  summary cards, progress chart, and filterable vulnerability table.
- **additional_fields:**
  - `labels`: ["ai-generated-jira"]
  - `priority`: {"name": "Major"}
  - `fixVersions`: [{"name": "RHTPA 1.5.0"}]
- **Tasks:** Task 4, Task 5, Task 6

### Documentation Task Assignment

- Task 7 (documentation) is assigned to **Epic 1: TC-9006: trustify-backend**

## Incorporates Links

Feature TC-9006 "Incorporates" the following Epics (NOT individual tasks):

- TC-9006 **Incorporates** Epic: TC-9006: trustify-backend
- TC-9006 **Incorporates** Epic: TC-9006: trustify-ui

## Impact Map

### trustify-backend

Changes:
- Add remediation model structs (`RemediationSummary`, `SeverityStatusCount`, `ProductRemediation`) in a new `remediation` domain module
- Add `RemediationService` with aggregation queries that compute remediation status from existing vulnerability and SBOM relationship data (no new tables)
- Add `GET /api/v2/remediation/summary` endpoint returning aggregated counts by severity and status
- Add `GET /api/v2/remediation/by-product` endpoint returning per-product remediation breakdown
- Register remediation routes in the server and mount under `/api/v2/remediation`
- Add integration tests for both remediation endpoints

### trustify-ui

Changes:
- Add TypeScript interfaces for remediation API response types (`RemediationSummary`, `ProductRemediation`)
- Add API client functions for remediation endpoints (`fetchRemediationSummary`, `fetchRemediationByProduct`)
- Add React Query hooks (`useRemediationSummary`, `useRemediationByProduct`)
- Add `RemediationDashboardPage` with summary cards (Open, In Progress, Resolved) and progress chart (30-day trend)
- Add filterable vulnerability table component with severity, product, and status filters
- Add `/remediation` route and navigation entry

## Non-MVP Requirements

| Requirement | Reason for deferral |
|---|---|
| Export remediation report as CSV | Marked as non-MVP in feature specification. Can be planned in a follow-up iteration once the core dashboard is delivered. |

## Excluded Requirements

None. All MVP requirements are fully specified and can be decomposed into actionable tasks.

## Task Dependency Order

```
Task 1 (backend model/service)
  -> Task 2 (backend endpoints) depends on Task 1
    -> Task 3 (backend tests) depends on Task 2
    -> Task 4 (frontend API/hooks) depends on Task 2
      -> Task 5 (frontend dashboard) depends on Task 4
        -> Task 6 (frontend table) depends on Task 5
Task 7 (documentation) depends on Tasks 2, 5, 6
```

Backend tasks (1-3) have lower task numbers than dependent frontend tasks (4-6),
ensuring correct implementation ordering.

## Inherited Field Values

- **Priority:** Major (inherited from Feature TC-9006)
- **fixVersions:** RHTPA 1.5.0 (inherited from Feature TC-9006; no `fixVersion scope` setting in CLAUDE.md, defaulting to "both" — propagated to all tasks)
- **Labels:** ai-generated-jira (applied to all created issues)

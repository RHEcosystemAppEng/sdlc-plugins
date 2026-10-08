# Repository Impact Map — TC-9006: Add vulnerability remediation tracking dashboard

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** All changes are additive — new endpoints, new module, new page, new components. No existing code is modified in a breaking way. The backend endpoints are new and do not alter existing API contracts. The frontend adds a new route and page that do not affect existing functionality. Each PR can land on `main` independently without leaving the codebase in a broken state. Dependency ordering ensures backend tasks complete before frontend tasks that consume the new endpoints. No atomicity indicators were identified:
- No coordinated schema migrations (no new database tables)
- No breaking API changes (all endpoints are new)
- No cross-cutting refactors
- Frontend and backend are in separate repositories; the frontend page is a new route that does not break existing pages if backend endpoints are not yet deployed

## Epic Hierarchy

**Grouping strategy:** by-repository (from CLAUDE.md Hierarchy Configuration)

**Level-1 issue type:** Epic (hierarchyLevel: 1)

### Epic 1: TC-9006: trustify-backend

- **Issue type:** Epic (level 1)
- **Summary:** TC-9006: trustify-backend
- **Parent:** TC-9006 (Feature)
- **Description:** Backend implementation for vulnerability remediation tracking. Adds a new remediation module to the trustify-backend service with two aggregation endpoints: a summary endpoint grouping vulnerability counts by severity and status, and a per-product breakdown endpoint. All aggregations computed from existing data without new database tables.
- **Creation parameters:**
  - `projectKey`: TC
  - `issueTypeName`: Epic
  - `parent`: TC-9006
  - `additional_fields`:
    - `labels`: ["ai-generated-jira"]
    - `priority`: {"name": "Major"}
    - `fixVersions`: [{"name": "RHTPA 1.5.0"}]
- **Assigned tasks:** Task 1, Task 2

### Epic 2: TC-9006: trustify-ui

- **Issue type:** Epic (level 1)
- **Summary:** TC-9006: trustify-ui
- **Parent:** TC-9006 (Feature)
- **Description:** Frontend implementation for the vulnerability remediation tracking dashboard. Adds API client integration, a new dashboard page at /remediation with summary cards, progress chart, and a filterable vulnerability table for drill-down by severity, product, and status.
- **Creation parameters:**
  - `projectKey`: TC
  - `issueTypeName`: Epic
  - `parent`: TC-9006
  - `additional_fields`:
    - `labels`: ["ai-generated-jira"]
    - `priority`: {"name": "Major"}
    - `fixVersions`: [{"name": "RHTPA 1.5.0"}]
- **Assigned tasks:** Task 3, Task 4, Task 5

### Documentation task Epic assignment

Task 6 (documentation) is assigned to Epic 1 (TC-9006: trustify-backend) as the primary documentation covers API endpoint reference hosted in the backend repository.

## Feature-to-Epic Links

Incorporates links are created from the Feature to each Epic (not to individual Tasks):

- TC-9006 **Incorporates** Epic 1 (TC-9006: trustify-backend)
- TC-9006 **Incorporates** Epic 2 (TC-9006: trustify-ui)

Tasks inherit hierarchy through their Epic parent field. No Feature-to-Task Incorporates links are created.

## Inherited Fields

- **Priority:** Major (inherited from Feature TC-9006, propagated to all Epics and Tasks)
- **Fix Versions:** RHTPA 1.5.0 (inherited from Feature TC-9006, propagated to all Epics and Tasks; `fixVersion scope` not configured in Jira Field Defaults, defaults to "both")

## Impact Map

### trustify-backend:
  changes:
    - Create remediation module with model/service/endpoints structure following existing domain module pattern
    - Implement `GET /api/v2/remediation/summary` endpoint returning aggregated counts by severity x status
    - Implement `GET /api/v2/remediation/by-product` endpoint returning per-product remediation breakdown with pagination
    - Add integration tests for both remediation endpoints
    - Mount remediation routes in server configuration

### trustify-ui:
  changes:
    - Add TypeScript interfaces for remediation API response types
    - Add API client functions for remediation endpoints
    - Add React Query hooks for remediation data fetching (useRemediationSummary, useRemediationByProduct)
    - Create RemediationDashboardPage at /remediation with summary cards and progress chart
    - Create filterable VulnerabilityTable component with severity, product, and status filters
    - Register /remediation route with lazy loading
    - Add MSW mock handlers and fixture data for remediation endpoints
    - Add unit tests for dashboard page and table components

## Task-to-Epic Assignments

| Task | Summary | Repository | Parent Epic |
|---|---|---|---|
| Task 1 | Add remediation module with summary aggregation endpoint | trustify-backend | TC-9006: trustify-backend |
| Task 2 | Add per-product remediation breakdown endpoint | trustify-backend | TC-9006: trustify-backend |
| Task 3 | Add API client functions and React Query hooks for remediation endpoints | trustify-ui | TC-9006: trustify-ui |
| Task 4 | Add remediation dashboard page with summary cards and progress chart | trustify-ui | TC-9006: trustify-ui |
| Task 5 | Add filterable vulnerability table to remediation dashboard | trustify-ui | TC-9006: trustify-ui |
| Task 6 | Document remediation dashboard and API endpoints | trustify-backend | TC-9006: trustify-backend |

## Task Dependency Graph

```
Task 1 (backend: summary endpoint)
  └─► Task 2 (backend: by-product endpoint)
        └─► Task 3 (frontend: API client + hooks)
              ├─► Task 4 (frontend: dashboard page)
              │     └─► Task 5 (frontend: vulnerability table)
              └─► Task 5 (frontend: vulnerability table)

Tasks 1-5 ──► Task 6 (documentation)
```

## Excluded Requirements

| Requirement | Reason |
|---|---|
| Export remediation report as CSV | Marked as non-MVP in the Feature description. Can be planned in a follow-up feature once the core dashboard is delivered. |

## Documentation Signals

- **Doc impact type:** New Content
- **Details:** Security teams need a guide for using the dashboard; API consumers need endpoint reference
- **Action:** Task 6 generated for documentation

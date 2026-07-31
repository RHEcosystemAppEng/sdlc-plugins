# Repository Impact Map -- TC-9006

## Feature: Add vulnerability remediation tracking dashboard

### trustify-backend

changes:
  - Add remediation module under `modules/fundamental/src/remediation/` following the existing model/ + service/ + endpoints/ structure
  - Create `RemediationSummary` and `ProductRemediation` model structs in `modules/fundamental/src/remediation/model/`
  - Create `RemediationService` with aggregation queries computing from existing vulnerability and SBOM relationship data (no new database tables) in `modules/fundamental/src/remediation/service/`
  - Create `GET /api/v2/remediation/summary` endpoint returning aggregated counts by severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved) in `modules/fundamental/src/remediation/endpoints/`
  - Create `GET /api/v2/remediation/by-product` endpoint returning per-product remediation breakdown (total, open, resolved counts) in `modules/fundamental/src/remediation/endpoints/`
  - Register remediation module routes in `server/src/main.rs`
  - Add integration tests for both remediation endpoints in `tests/api/remediation.rs`

### trustify-ui

changes:
  - Add TypeScript interfaces for remediation API response types in `src/api/models.ts`
  - Add API client functions (`fetchRemediationSummary()`, `fetchRemediationByProduct()`) in `src/api/rest.ts`
  - Add React Query hooks (`useRemediationSummary`, `useRemediationByProduct`) in `src/hooks/`
  - Create `RemediationDashboardPage` at `/remediation` with summary cards (Open, In Progress, Resolved counts) and progress chart (trend over 30 days) in `src/pages/RemediationDashboardPage/`
  - Add filterable vulnerability table component with filters for severity, product, and status in `src/pages/RemediationDashboardPage/components/`
  - Register `/remediation` route in `src/routes.tsx`
  - Add unit tests (Vitest + React Testing Library) and E2E tests (Playwright) for the remediation dashboard
  - Add MSW mock handlers and fixture data for remediation endpoints in `tests/mocks/`

### Excluded requirements

- **CSV export for remediation report** (non-MVP) -- the feature lists `Export remediation report as CSV` as a non-MVP requirement. This can be planned as a follow-up feature once the MVP dashboard is delivered.

## Epic Grouping (by-repository)

| Epic | Tasks |
|---|---|
| TC-9006: trustify-backend | Task 2, Task 3 |
| TC-9006: trustify-ui | Task 1 (bookend), Task 4, Task 5, Task 6, Task 7, Task 8 (doc), Task 9 (bookend) |

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** Atomicity indicator #4 (Tightly coupled feature components) is present -- the frontend RemediationDashboardPage requires the new backend `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product` endpoints that do not yet exist. Merging the frontend without the backend would result in a non-functional dashboard page. Merging the backend alone would be safe but the feature is not useful without the frontend. The feature branch ensures all components land on main together.

**Interdependent tasks:**
- Backend Tasks 2-3 (remediation endpoints) are required by Frontend Tasks 4-7 (API client, dashboard page, table, tests)
- Frontend Task 5 (dashboard page) calls endpoints defined in Backend Task 2
- Frontend Task 4 (API hooks) depends on the response shapes from Backend Task 2

The `workflow:feature-branch` label will be applied to the feature issue TC-9006.

## Inherited Field Values

- **Priority:** Major (propagated to all tasks and Epics)
- **fixVersions:** RHTPA 1.5.0 (propagated to all tasks and Epics; no fixVersion scope override in Jira Field Defaults -- defaults to "both")

## Task Creation Log -- additional_fields

Every task and Epic created includes the following `additional_fields`:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

Bookend tasks also include `"labels": ["ai-generated-jira"]` with the same priority and fixVersions.

The feature issue TC-9006 receives the additional label `workflow:feature-branch` appended to its existing labels.

## Type-to-Role Mapping

```
Type-to-role mapping:
  Feature: Feature (ID: 10142, level: 2)
  Epic:    Epic (ID: <discovered>, level: 1)
  Task:    Task (ID: <discovered>, level: 0)
```

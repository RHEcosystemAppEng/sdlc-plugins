# Repository Impact Map -- TC-9006: Add vulnerability remediation tracking dashboard

## Impact Map

```
trustify-backend:
  changes:
    - Add remediation module with model/service/endpoints structure under modules/fundamental/src/remediation/
    - Add GET /api/v2/remediation/summary endpoint for aggregated counts by severity and status
    - Add GET /api/v2/remediation/by-product endpoint for per-product remediation breakdown
    - Register remediation routes in server/src/main.rs
    - Add integration tests for both remediation endpoints in tests/api/remediation.rs

trustify-ui:
  changes:
    - Add TypeScript interfaces for remediation API response types in src/api/models.ts
    - Add API client functions (fetchRemediationSummary, fetchRemediationByProduct) in src/api/rest.ts
    - Add React Query hooks (useRemediationSummary, useRemediationByProduct) in src/hooks/
    - Add RemediationDashboardPage at /remediation with summary cards and progress chart
    - Add filterable vulnerability table with severity, product, and status filters
    - Add route definition for /remediation in src/routes.tsx
    - Document the remediation dashboard and aggregation endpoints
```

## Workflow Mode Decision

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified:
- No coordinated schema migrations -- no new database tables; aggregations computed from existing data
- No breaking API changes -- both endpoints are new additions, no modifications to existing APIs
- No cross-cutting refactors -- changes are additive in both repositories
- Frontend and backend are not tightly coupled for deployment purposes -- backend endpoints can land first as additive changes, and the frontend dashboard page is a new route that can land after the backend is available. Neither side breaks `main` when merged independently, provided backend lands before frontend.

## Epic Hierarchy

### Grouping Strategy
`by-repository` (from CLAUDE.md Hierarchy Configuration default)

### Epic 1: TC-9006: trustify-backend
- **Issue type:** Epic (hierarchyLevel: 1)
- **Parent:** TC-9006 (Feature)
- **Summary:** TC-9006: trustify-backend
- **Description:** Backend remediation aggregation endpoints for the vulnerability remediation tracking dashboard. Includes the summary endpoint, by-product endpoint, and integration tests.
- **additional_fields:**
  ```json
  {
    "labels": ["ai-generated-jira"],
    "priority": {"name": "Major"},
    "fixVersions": [{"name": "RHTPA 1.5.0"}]
  }
  ```
- **Tasks assigned:**
  - Task 1: Add remediation summary aggregation service and endpoint
  - Task 2: Add remediation by-product aggregation service and endpoint
  - Task 3: Add integration tests for remediation endpoints

### Epic 2: TC-9006: trustify-ui
- **Issue type:** Epic (hierarchyLevel: 1)
- **Parent:** TC-9006 (Feature)
- **Summary:** TC-9006: trustify-ui
- **Description:** Frontend remediation dashboard for the vulnerability remediation tracking feature. Includes API client layer, dashboard page with summary cards and progress chart, filterable vulnerability table, and documentation.
- **additional_fields:**
  ```json
  {
    "labels": ["ai-generated-jira"],
    "priority": {"name": "Major"},
    "fixVersions": [{"name": "RHTPA 1.5.0"}]
  }
  ```
- **Tasks assigned:**
  - Task 4: Add API client functions and React Query hooks for remediation endpoints
  - Task 5: Add remediation dashboard page with summary cards and progress chart
  - Task 6: Add filterable vulnerability table to remediation dashboard
  - Task 7: Document the remediation dashboard and aggregation endpoints

## Incorporates Links

Feature-to-Epic "Incorporates" links (NOT Feature-to-Task):
- TC-9006 --[Incorporates]--> Epic 1 (TC-9006: trustify-backend)
- TC-9006 --[Incorporates]--> Epic 2 (TC-9006: trustify-ui)

## Task-to-Epic Parent Assignment

Each task's `parent` field is set to its assigned Epic key:
- Task 1 (backend): parent = Epic 1 key (TC-9006: trustify-backend)
- Task 2 (backend): parent = Epic 1 key (TC-9006: trustify-backend)
- Task 3 (backend): parent = Epic 1 key (TC-9006: trustify-backend)
- Task 4 (frontend): parent = Epic 2 key (TC-9006: trustify-ui)
- Task 5 (frontend): parent = Epic 2 key (TC-9006: trustify-ui)
- Task 6 (frontend): parent = Epic 2 key (TC-9006: trustify-ui)
- Task 7 (documentation): parent = Epic 2 key (TC-9006: trustify-ui)

## Task additional_fields

All tasks are created with the following additional_fields:
```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

- **Priority:** inherited from Feature TC-9006 (Major). Priority is not "Undefined", so it is propagated.
- **fixVersions:** inherited from Feature TC-9006 (RHTPA 1.5.0). Feature has non-empty fixVersions, and no `fixVersion scope` setting exists in Jira Field Defaults, so the default "both" applies -- fixVersions are propagated to tasks.

## Excluded Requirements

- **Export remediation report as CSV** -- marked as non-MVP in the feature requirements (Is MVP: No). This requirement is not included in the current plan. It can be planned as a follow-up feature after the core dashboard is delivered.

## Conventions Discovered

- **trustify-backend** -- `CONVENTIONS.md` found at repo root. Key conventions applied: Module Pattern (model/ + service/ + endpoints/), Error Handling (Result<T, AppError>), Endpoint Registration, Response Types (PaginatedResults<T>), Query Helpers, Testing (integration tests with PostgreSQL).
- **trustify-ui** -- `CONVENTIONS.md` found at repo root. Key conventions applied: API Layer (Axios client, rest.ts, hooks), Page Structure (pages/<PageName>/), Component Library (PatternFly 5), State Management (React Query), Naming (PascalCase/camelCase), Testing (Vitest + RTL + MSW).

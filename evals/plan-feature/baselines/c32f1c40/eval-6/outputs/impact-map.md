# Repository Impact Map

## Feature: TC-9006 — Add vulnerability remediation tracking dashboard

### Workflow Mode: `feature-branch`

**Rationale:** Tightly coupled feature components -- the frontend remediation dashboard page at `/remediation` requires backend API endpoints (`GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`) that do not yet exist. Merging the frontend without the backend would result in a page that calls non-existent endpoints. This satisfies atomicity indicator #4 (tightly coupled feature components where neither side functions independently).

**Interdependent tasks:** Frontend tasks (API types, dashboard page, vulnerability table) depend on backend tasks (remediation service, endpoints) -- the frontend cannot function without the backend endpoints being available.

The `workflow:feature-branch` label will be applied to the feature issue TC-9006 in Step 6a.

---

### Impact Map

```
trustify-backend:
  changes:
    - Add remediation data models (RemediationSummary, ProductRemediation structs) and aggregation service in a new remediation module under modules/fundamental/src/remediation/
    - Add GET /api/v2/remediation/summary endpoint returning aggregated vulnerability counts grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved)
    - Add GET /api/v2/remediation/by-product endpoint returning per-product remediation breakdown with total, open, and resolved counts
    - Register remediation routes in server/src/main.rs
    - Add integration tests for both remediation endpoints in tests/api/remediation.rs

trustify-ui:
  changes:
    - Add TypeScript interfaces for remediation API response types in src/api/models.ts
    - Add API client functions for fetching remediation data in src/api/rest.ts
    - Add React Query hooks for remediation summary and by-product data in src/hooks/
    - Create RemediationDashboard page directory under src/pages/ with summary cards and progress chart
    - Add route definition for /remediation in src/routes.tsx
    - Create filterable vulnerability table component with severity, product, and status filters
    - Add unit tests (Vitest + React Testing Library) and MSW mock handlers for the remediation dashboard
    - Add E2E test for the remediation dashboard page
```

### Excluded requirements

- **Export remediation report as CSV** (Non-MVP requirement) -- The feature description marks this as non-MVP. Deferred to a future planning iteration. When prioritized, this will require a backend CSV export endpoint and a frontend export button on the remediation dashboard.

---

## Epic Hierarchy

### Grouping Strategy: `by-repository`

Source: CLAUDE.md `## Hierarchy Configuration` -- `Default epic grouping strategy: by-repository`

### Epics to Create

| Epic Summary | Issue Type | Parent | Repository Group |
|---|---|---|---|
| TC-9006: trustify-backend | Epic (level 1) | TC-9006 | Backend tasks (Tasks 2-4) |
| TC-9006: trustify-ui | Epic (level 1) | TC-9006 | Frontend + bookend + documentation tasks (Tasks 1, 5-10) |

### Epic Creation Details

**Epic: TC-9006: trustify-backend**
- Issue type: Epic
- Parent: TC-9006
- Summary: TC-9006: trustify-backend
- Description: Backend implementation for the vulnerability remediation tracking dashboard. Includes remediation data models, aggregation service, REST endpoints for summary and by-product views, and integration tests.
- additional_fields:
  ```json
  {
    "labels": ["ai-generated-jira"],
    "priority": {"name": "Major"},
    "fixVersions": [{"name": "RHTPA 1.5.0"}]
  }
  ```

**Epic: TC-9006: trustify-ui**
- Issue type: Epic
- Parent: TC-9006
- Summary: TC-9006: trustify-ui
- Description: Frontend implementation for the vulnerability remediation tracking dashboard. Includes API types and React Query hooks, dashboard page with summary cards and progress chart, filterable vulnerability table, unit and E2E tests, feature branch management, and documentation.
- additional_fields:
  ```json
  {
    "labels": ["ai-generated-jira"],
    "priority": {"name": "Major"},
    "fixVersions": [{"name": "RHTPA 1.5.0"}]
  }
  ```

### Incorporates Links (Feature to Epics)

| From | Link Type | To |
|---|---|---|
| TC-9006 | Incorporates | TC-9006: trustify-backend (Epic) |
| TC-9006 | Incorporates | TC-9006: trustify-ui (Epic) |

Note: Incorporates links go from the Feature to each Epic, NOT from the Feature to individual Tasks. Tasks inherit hierarchy through their Epic parent.

### Task-to-Epic Assignment

| Task | Repository | Parent Epic |
|---|---|---|
| Task 1 -- Create feature branch TC-9006 from main | trustify-ui | TC-9006: trustify-ui |
| Task 2 -- Add remediation data models and aggregation service | trustify-backend | TC-9006: trustify-backend |
| Task 3 -- Add remediation summary and by-product REST endpoints | trustify-backend | TC-9006: trustify-backend |
| Task 4 -- Add remediation endpoint integration tests | trustify-backend | TC-9006: trustify-backend |
| Task 5 -- Add remediation API types, client functions, and React Query hooks | trustify-ui | TC-9006: trustify-ui |
| Task 6 -- Create remediation dashboard page with summary cards and progress chart | trustify-ui | TC-9006: trustify-ui |
| Task 7 -- Add filterable vulnerability table to remediation dashboard | trustify-ui | TC-9006: trustify-ui |
| Task 8 -- Add remediation dashboard unit and E2E tests | trustify-ui | TC-9006: trustify-ui |
| Task 9 -- Document remediation dashboard and aggregation endpoints | trustify-ui | TC-9006: trustify-ui |
| Task 10 -- Merge feature branch TC-9006 to main | trustify-ui | TC-9006: trustify-ui |

---

## Inherited Field Values

- **Priority**: Major (inherited from Feature TC-9006, propagated to all Epics and Tasks)
- **Fix Versions**: RHTPA 1.5.0 (inherited from Feature TC-9006, propagated to all Epics and Tasks; fixVersion scope defaults to "both" since no Jira Field Defaults section exists in CLAUDE.md)

## Documentation Signals

- **Doc impact type**: New Content
- **Details**: Document the remediation dashboard and aggregation endpoints. Security teams need a guide for using the dashboard; API consumers need endpoint reference.
- **Action**: Documentation task (Task 9) generated to cover this requirement.

## Task additional_fields

All tasks are created with the following `additional_fields`:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

Each task's `parent` field is set to its assigned Epic key (resolved after Epic creation).

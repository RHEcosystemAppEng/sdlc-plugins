# Repository Impact Map — TC-9006: Add vulnerability remediation tracking dashboard

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. The backend and frontend live in separate repositories (`trustify-backend` and `trustify-ui`). The backend adds new API endpoints (not breaking changes to existing ones), so it can be merged to `main` independently. The frontend depends on the backend endpoints being available but can be merged after the backend lands. No coordinated schema migrations are required (the feature explicitly states "No new database tables"). No cross-cutting refactors span multiple tasks. Each side functions independently at the code level — the backend endpoints are additive and the frontend can be merged once the backend is deployed.

## Impact Map

```
trustify-backend:
  changes:
    - Add remediation module with model structs (RemediationSummary, ProductRemediation) and aggregation service layer
    - Add GET /api/v2/remediation/summary endpoint returning aggregated counts by severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved)
    - Add GET /api/v2/remediation/by-product endpoint returning per-product remediation breakdown (total, open, resolved counts)
    - Register remediation module routes in server/src/main.rs
    - Add integration tests for remediation endpoints in tests/api/
    - Add GET /api/v2/remediation/export/csv endpoint for CSV report export (non-MVP)

trustify-ui:
  changes:
    - Add TypeScript interfaces for remediation API response types (RemediationSummary, ProductRemediation)
    - Add API client functions for remediation endpoints (fetchRemediationSummary, fetchRemediationByProduct)
    - Add React Query hooks for remediation data fetching (useRemediationSummary, useRemediationByProduct)
    - Add RemediationDashboardPage at /remediation with summary cards and progress chart
    - Add filterable vulnerability table component to the dashboard with severity, product, and status filters
    - Register /remediation route in React Router configuration
    - Add MSW mock handlers and fixtures for remediation endpoints
```

## Excluded Requirements

(none -- all requirements from the Feature description can be decomposed into actionable tasks)

## Epic Hierarchy

**Grouping strategy:** `by-repository` (from CLAUDE.md Hierarchy Configuration)

**Level-1 issue type:** Epic (hierarchyLevel: 1)

### Epics to Create

| Epic | Summary | Issue Type | Parent | Description |
|---|---|---|---|---|
| Epic 1 (simulated key: TC-9007) | TC-9006: trustify-backend | Epic | TC-9006 | Backend remediation module: model structs, aggregation service, REST API endpoints (summary, by-product, CSV export), and integration tests. |
| Epic 2 (simulated key: TC-9008) | TC-9006: trustify-ui | Epic | TC-9006 | Frontend remediation dashboard: API client layer, React Query hooks, dashboard page with summary cards, progress chart, and filterable vulnerability table. |

### Task-to-Epic Assignment

| Task | Epic |
|---|---|
| Task 1 — Add remediation model and service layer | TC-9007 (trustify-backend) |
| Task 2 — Add remediation API endpoints with integration tests | TC-9007 (trustify-backend) |
| Task 3 — Add CSV export endpoint for remediation report | TC-9007 (trustify-backend) |
| Task 4 — Add remediation API client and React Query hooks | TC-9008 (trustify-ui) |
| Task 5 — Add remediation dashboard page with summary cards and progress chart | TC-9008 (trustify-ui) |
| Task 6 — Add filterable vulnerability table to remediation dashboard | TC-9008 (trustify-ui) |
| Task 7 — Document remediation dashboard and aggregation endpoints | TC-9007 (trustify-backend) |

### Issue Links

**Feature "Incorporates" Epic links (not Feature-to-Task):**
- TC-9006 Incorporates TC-9007 (TC-9006: trustify-backend)
- TC-9006 Incorporates TC-9008 (TC-9006: trustify-ui)

**Task "Depends on" Task links:**
- Task 2 depends on Task 1
- Task 3 depends on Task 2
- Task 4 depends on Task 2
- Task 5 depends on Task 4
- Task 6 depends on Task 5
- Task 7 depends on Tasks 2, 3, 5, 6

## additional_fields for Created Issues

### Epics

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

Each Epic is created with:
- `issueTypeName`: "Epic" (level-1 type)
- `parent`: TC-9006 (the Feature issue key)
- `additional_fields` as shown above

### Tasks

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

Each task is created with:
- `parent`: its assigned Epic key (TC-9007 for backend tasks, TC-9008 for frontend tasks)
- `additional_fields` as shown above

**Field propagation rationale:**
- `priority`: "Major" inherited from Feature TC-9006 (not "Undefined", so propagated)
- `fixVersions`: "RHTPA 1.5.0" inherited from Feature TC-9006 (Feature has non-empty fixVersions; no `fixVersion scope` setting in Jira Field Defaults — defaults to "both", so propagated to tasks)

## Documentation Signals

- **Doc impact type:** New Content
- **Details:** Security teams need a guide for using the dashboard; API consumers need endpoint reference
- **Action:** Generate documentation task (Task 7)

# Repository Impact Map -- TC-9006

## Type-to-Role Mapping

| Role | Type Name | Type ID | Hierarchy Level |
|---|---|---|---|
| Feature | Feature | 10142 | 2 |
| Epic | Epic | (discovered dynamically) | 1 |
| Task | Task | (discovered dynamically) | 0 |

## Epic Grouping

**Strategy**: by-repository (from CLAUDE.md Hierarchy Configuration)

| Epic | Summary | Repository |
|---|---|---|
| Epic 1 | TC-9006: trustify-backend | trustify-backend |
| Epic 2 | TC-9006: trustify-ui | trustify-ui |

Epic descriptions:
- **TC-9006: trustify-backend** -- Backend remediation module with aggregation service and REST endpoints for vulnerability remediation summary and per-product breakdown.
- **TC-9006: trustify-ui** -- Frontend remediation dashboard page with summary cards, progress chart, filterable vulnerability table, and supporting API client layer.

## Impact Map

### trustify-backend

Changes:
- Add remediation module following the established model/ + service/ + endpoints/ pattern under modules/fundamental/src/
- Add `GET /api/v2/remediation/summary` endpoint returning aggregated counts by severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved)
- Add `GET /api/v2/remediation/by-product` endpoint returning per-product remediation breakdown with total, open, in-progress, and resolved counts
- Mount remediation routes in server/src/main.rs
- Add integration tests for both remediation endpoints in tests/api/

### trustify-ui

Changes:
- Add TypeScript interfaces for remediation API response types in src/api/models.ts
- Add API client functions for remediation endpoints in src/api/rest.ts
- Add React Query hooks for remediation summary and by-product data
- Create RemediationDashboardPage at /remediation with summary cards, progress chart, and filterable vulnerability table
- Add /remediation route to router configuration in src/routes.tsx
- Add MSW mock handlers and test fixtures for remediation API endpoints
- Add unit tests for dashboard page and components

## Excluded Requirements

| Requirement | Reason |
|---|---|
| Export remediation report as CSV | Marked as non-MVP in the Feature description. Can be planned in a follow-up iteration once the core dashboard is delivered. |

## Workflow Mode Decision

**Selected mode**: `direct-to-main`

**Rationale**: No atomicity indicators identified:
1. **No coordinated schema migrations** -- the Feature requirement explicitly states "No new database tables -- compute aggregations from existing vulnerability and SBOM relationship data." No schema changes are needed.
2. **No breaking API changes** -- both backend endpoints (`/api/v2/remediation/summary` and `/api/v2/remediation/by-product`) are new additions that do not modify existing API contracts.
3. **No cross-cutting refactors** -- all changes are additive (new remediation module in backend, new dashboard page in frontend). No existing code is restructured.
4. **No tightly coupled components requiring simultaneous deployment** -- the backend endpoints are additive REST endpoints that can be merged and deployed independently. The frontend adds a new page at a new route (`/remediation`) without affecting existing pages.

No `workflow:feature-branch` label will be applied to the feature issue. All tasks target the `main` branch.

## Inherited Field Values

The following fields are inherited from Feature TC-9006 and propagated to all created Epics and Tasks:

| Field | Value | Propagation Rule | Propagated? |
|---|---|---|---|
| Priority | Major | Feature has a defined priority (not "Undefined") | Yes |
| Fix Versions | RHTPA 1.5.0 | Feature has fixVersions set; no `fixVersion scope` setting in Jira Field Defaults (defaults to "both") | Yes |
| Labels | ai-generated-jira | Required on all created issues per skill rules | Yes |

### additional_fields for Epics

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

Parent field: `{"parent": {"key": "TC-9006"}}`

### additional_fields for Tasks

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

Parent field: `{"parent": {"key": "<assigned-epic-key>"}}` (Epic key from sub-step 6a.0)

## Task Assignment

| Task # | Summary | Epic | Repository |
|---|---|---|---|
| 1 | Add remediation module with summary aggregation endpoint | TC-9006: trustify-backend | trustify-backend |
| 2 | Add remediation by-product breakdown endpoint | TC-9006: trustify-backend | trustify-backend |
| 3 | Add remediation endpoint integration tests | TC-9006: trustify-backend | trustify-backend |
| 4 | Add remediation API types, client functions, and React Query hooks | TC-9006: trustify-ui | trustify-ui |
| 5 | Create remediation dashboard page with summary cards and progress chart | TC-9006: trustify-ui | trustify-ui |
| 6 | Add filterable vulnerability table to remediation dashboard | TC-9006: trustify-ui | trustify-ui |
| 7 | Document remediation dashboard and API endpoints | TC-9006: trustify-ui | trustify-ui |

## Task Dependencies

- Task 2 depends on Task 1
- Task 3 depends on Task 1, Task 2
- Task 4 depends on Task 1, Task 2
- Task 5 depends on Task 4
- Task 6 depends on Task 4
- Task 7 depends on Tasks 1, 2, 3, 4, 5, 6

## Documentation Signals

Extracted from Feature description "Documentation Considerations" section:
- **Doc impact type**: New Content
- **Details**: Document the remediation dashboard and aggregation endpoints. Security teams need a guide for using the dashboard; API consumers need endpoint reference.

## Issue Links

### Feature "incorporates" Epics
- TC-9006 incorporates Epic 1 (TC-9006: trustify-backend)
- TC-9006 incorporates Epic 2 (TC-9006: trustify-ui)

### Task "depends on" Links
- Task 2 depends on Task 1
- Task 3 depends on Task 1
- Task 3 depends on Task 2
- Task 4 depends on Task 1
- Task 4 depends on Task 2
- Task 5 depends on Task 4
- Task 6 depends on Task 4
- Task 7 depends on Task 1
- Task 7 depends on Task 2
- Task 7 depends on Task 3
- Task 7 depends on Task 4
- Task 7 depends on Task 5
- Task 7 depends on Task 6

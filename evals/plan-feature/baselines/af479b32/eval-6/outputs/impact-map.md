# Repository Impact Map — TC-9006

## Impact Map

```
trustify-backend:
  changes:
    - Create remediation module following existing module pattern (model/ + service/ + endpoints/)
    - Add RemediationSummary and ProductRemediation model structs for aggregation response types
    - Create RemediationService with aggregation queries over existing advisory and SBOM entity relationships (no new tables)
    - Add GET /api/v2/remediation/summary endpoint returning aggregated counts by severity x status
    - Add GET /api/v2/remediation/by-product endpoint returning per-product remediation breakdown
    - Register remediation routes in server/src/main.rs
    - Add CSV export endpoint for remediation report (non-MVP)
    - Add integration tests for all new endpoints in tests/api/

trustify-ui:
  changes:
    - Add TypeScript interfaces for remediation API response types in src/api/models.ts
    - Add API client functions for remediation endpoints in src/api/rest.ts
    - Add React Query hooks for remediation summary and by-product data in src/hooks/
    - Create RemediationDashboardPage at /remediation with summary cards and progress chart
    - Add filterable vulnerability table component with severity, product, and status filters
    - Register /remediation route in src/routes.tsx
    - Add unit tests and mock fixtures for the remediation dashboard
```

## Excluded Requirements

None. All MVP and non-MVP requirements from the Feature description can be decomposed into actionable tasks. The CSV export requirement (non-MVP) is included as a separate task.

## Workflow Mode Decision

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified:

1. **Coordinated schema migrations:** Not applicable. The NFRs explicitly state "No new database tables" — aggregations are computed from existing vulnerability and SBOM relationship data.
2. **Breaking API changes:** Not applicable. All backend changes are additive new endpoints (`/api/v2/remediation/summary` and `/api/v2/remediation/by-product`). No existing endpoints are modified.
3. **Cross-cutting refactors:** Not applicable. No existing modules, types, or shared code are being reorganized.
4. **Tightly coupled feature components:** Not applicable with dependency ordering. The backend remediation endpoints are independently functional (they serve data for API consumers regardless of the dashboard). The frontend dashboard depends on the backend endpoints, but explicit task dependencies ensure backend PRs merge to main before frontend PRs are started. Each PR leaves main in a working state.

All tasks use Target Branch: `main`.

## Epic Grouping

**Strategy:** `by-repository` (from CLAUDE.md Hierarchy Configuration)

| Epic | Group Label | Tasks |
|---|---|---|
| TC-9006: trustify-backend | trustify-backend | Task 1, Task 2, Task 6 |
| TC-9006: trustify-ui | trustify-ui | Task 3, Task 4, Task 5 |

Documentation task (Task 7) is assigned to the trustify-backend Epic since the primary documentation deliverable is the API endpoint reference.

## Epic Creation Details

### Epic 1: TC-9006: trustify-backend

- **Issue type:** Epic (hierarchyLevel 1)
- **Summary:** TC-9006: trustify-backend
- **Description:** Backend implementation for the vulnerability remediation tracking dashboard. Creates the remediation module with aggregation service, summary and by-product endpoints, and CSV export capability. All aggregations compute over existing advisory and SBOM entity relationships with no new database tables.
- **Parent:** TC-9006
- **additional_fields:**
  ```json
  {
    "labels": ["ai-generated-jira"],
    "priority": {"name": "Major"},
    "fixVersions": [{"name": "RHTPA 1.5.0"}]
  }
  ```

### Epic 2: TC-9006: trustify-ui

- **Issue type:** Epic (hierarchyLevel 1)
- **Summary:** TC-9006: trustify-ui
- **Description:** Frontend implementation for the vulnerability remediation tracking dashboard. Creates the remediation dashboard page at /remediation with summary cards, progress chart, and filterable vulnerability table using PatternFly components and React Query for data fetching.
- **Parent:** TC-9006
- **additional_fields:**
  ```json
  {
    "labels": ["ai-generated-jira"],
    "priority": {"name": "Major"},
    "fixVersions": [{"name": "RHTPA 1.5.0"}]
  }
  ```

## Issue Links

### Feature "Incorporates" links (Feature to Epics)

- TC-9006 **Incorporates** Epic 1 (TC-9006: trustify-backend)
- TC-9006 **Incorporates** Epic 2 (TC-9006: trustify-ui)

### Task parent assignments

- Tasks 1, 2, 6, 7 → parent: Epic 1 (trustify-backend)
- Tasks 3, 4, 5 → parent: Epic 2 (trustify-ui)

## Inherited Fields

All Epics and Tasks inherit the following from Feature TC-9006:

- **Priority:** Major (propagated because Feature priority is set and not "Undefined")
- **Fix Versions:** RHTPA 1.5.0 (propagated because Feature has fixVersions set and no `fixVersion scope` restriction is configured in Jira Field Defaults — defaults to "both")

## additional_fields for all created issues

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

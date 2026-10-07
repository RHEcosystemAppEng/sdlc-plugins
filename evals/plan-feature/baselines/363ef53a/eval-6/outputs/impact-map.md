# Repository Impact Map — TC-9006

## Changes by Repository

### trustify-backend
Changes:
- Add `remediation` module under `modules/fundamental/src/` with model structs (RemediationSummary, SeverityBreakdown, StatusBreakdown, ProductRemediation) and aggregation service
- Add REST endpoint `GET /api/v2/remediation/summary` returning aggregated counts by severity and status
- Add REST endpoint `GET /api/v2/remediation/by-product` returning per-product remediation breakdown with pagination
- Register remediation routes in `server/src/main.rs`
- Add integration tests for remediation endpoints in `tests/api/remediation.rs`
- Add documentation for remediation dashboard and API endpoints

### trustify-ui
Changes:
- Add TypeScript interfaces for remediation API response types in `src/api/models.ts`
- Add API client functions (fetchRemediationSummary, fetchRemediationByProduct) in `src/api/rest.ts`
- Add React Query hooks (useRemediationSummary, useRemediationByProduct) in `src/hooks/`
- Add RemediationDashboardPage at `/remediation` with summary cards and progress chart
- Add filterable VulnerabilityTable component with severity, product, and status filters
- Register `/remediation` route in `src/routes.tsx` and add navigation entry in `src/App.tsx`
- Add component tests for the remediation dashboard page

## Excluded Requirements

- **Export remediation report as CSV** — marked as non-MVP in the Feature requirements. The endpoint specification is clear, but it is deferred to a future iteration to focus on the core dashboard MVP.

## Epic Hierarchy

Epic grouping strategy: **by-repository** (from CLAUDE.md Hierarchy Configuration)

Level-1 issue type: **Epic** (hierarchyLevel 1)

### Epics

| Epic | Summary | Parent | Tasks |
|---|---|---|---|
| Epic 1 | TC-9006: trustify-backend | TC-9006 | Task 1, Task 2, Task 3, Task 7 |
| Epic 2 | TC-9006: trustify-ui | TC-9006 | Task 4, Task 5, Task 6 |

### Epic creation parameters

Each Epic is created with:
- Issue type: Epic (level-1 type)
- Parent: TC-9006 (the Feature issue)
- Labels: `["ai-generated-jira"]`
- Priority: `{"name": "Major"}` (inherited from Feature)
- Fix Versions: `[{"name": "RHTPA 1.5.0"}]` (inherited from Feature)

### Incorporates links

Links are created from the Feature to each **Epic** (not to individual Tasks):
- TC-9006 **incorporates** Epic 1 (TC-9006: trustify-backend)
- TC-9006 **incorporates** Epic 2 (TC-9006: trustify-ui)

Tasks inherit hierarchy through their Epic parent field — no direct Feature-to-Task links are needed.

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified:

1. **Coordinated schema migrations:** Not present. The feature explicitly requires no new database tables — aggregations are computed from existing data.
2. **Breaking API changes:** Not present. Both backend endpoints (`GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`) are brand-new additions that do not modify any existing API contracts.
3. **Cross-cutting refactors:** Not present. All changes are additive — a new backend module and a new frontend page, with no modifications to existing modules or shared interfaces.
4. **Tightly coupled feature components:** The frontend dashboard requires the backend endpoints, but the repositories are independent with separate deployment pipelines. The backend can be merged and deployed first (new endpoints are additive and do not affect existing functionality), and the frontend can follow. Neither side breaks `main` when merged independently.

All tasks target branch: `main`.

## Inherited Fields

Fields inherited from Feature TC-9006 and propagated to all created Epics and Tasks:

| Field | Value | Propagated | Rationale |
|---|---|---|---|
| Priority | Major | Yes | Feature priority is "Major" (not "Undefined"), so it is propagated to all Epics and Tasks |
| Fix Versions | RHTPA 1.5.0 | Yes | Feature has non-empty fixVersions; no Jira Field Defaults section exists, so fixVersion scope defaults to "both" — propagated to both Epics and Tasks |
| Labels | ai-generated-jira | Yes | Required on all AI-generated issues |

### additional_fields for Epic creation

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

Parent field: `{"key": "TC-9006"}`

### additional_fields for Task creation

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

Parent field: set to the assigned Epic key (Epic 1 for backend tasks, Epic 2 for frontend tasks)

## Task Summary

| # | Summary | Repository | Epic | Dependencies |
|---|---|---|---|---|
| 1 | Add remediation module with model structs and aggregation service | trustify-backend | TC-9006: trustify-backend | None |
| 2 | Add remediation REST endpoints | trustify-backend | TC-9006: trustify-backend | Task 1 |
| 3 | Add integration tests for remediation endpoints | trustify-backend | TC-9006: trustify-backend | Task 2 |
| 4 | Add API client and React Query hooks for remediation endpoints | trustify-ui | TC-9006: trustify-ui | Task 2 |
| 5 | Add remediation dashboard page with summary cards and progress chart | trustify-ui | TC-9006: trustify-ui | Task 4 |
| 6 | Add filterable vulnerability table to remediation dashboard | trustify-ui | TC-9006: trustify-ui | Task 5 |
| 7 | Document remediation dashboard and aggregation endpoints | trustify-backend | TC-9006: trustify-backend | Tasks 1-6 |

## Documentation Signals

- **Doc impact type:** New Content
- **Details:** Security teams need a guide for using the dashboard; API consumers need endpoint reference
- **Action:** Task 7 covers documentation generation

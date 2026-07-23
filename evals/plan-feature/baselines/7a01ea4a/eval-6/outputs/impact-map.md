# Repository Impact Map -- TC-9006

## Feature

**TC-9006**: Add vulnerability remediation tracking dashboard

**Priority**: Major (inherited by tasks)
**Fix Versions**: RHTPA 1.5.0 (inherited by tasks)

## Impact Map

### trustify-backend

**Changes:**
- Create a new `remediation` module under `modules/fundamental/src/` following the existing `model/ + service/ + endpoints/` module pattern (as used by `sbom`, `advisory`, `package`)
- Implement `RemediationSummary` model struct to represent aggregated counts grouped by severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved)
- Implement `ProductRemediation` model struct to represent per-product remediation breakdown (total, open, resolved counts per product)
- Implement `RemediationService` with methods to compute aggregations from existing `advisory`, `sbom_advisory`, and related entity tables -- no new database tables
- Add `GET /api/v2/remediation/summary` endpoint returning aggregated remediation counts by severity and status
- Add `GET /api/v2/remediation/by-product` endpoint returning per-product remediation breakdown
- Add `GET /api/v2/remediation/export` endpoint returning CSV-formatted remediation report (non-MVP)
- Register remediation routes in `server/src/main.rs`
- Add integration tests in `tests/api/remediation.rs`

### trustify-ui

**Changes:**
- Add TypeScript interfaces for remediation API response types in `src/api/models.ts`
- Add API client functions (`fetchRemediationSummary()`, `fetchRemediationByProduct()`) in `src/api/rest.ts`
- Add React Query hooks (`useRemediationSummary`, `useRemediationByProduct`) in `src/hooks/`
- Create `RemediationDashboardPage` under `src/pages/RemediationDashboardPage/` with summary cards (Open, In Progress, Resolved counts) and a progress chart (30-day trend)
- Create a filterable vulnerability table component supporting severity, product, and status filters using PatternFly `FilterToolbar`
- Add `/remediation` route in `src/routes.tsx`
- Add unit tests for the dashboard page and components

## Excluded Requirements

_None -- all requirements from the Feature description have been decomposed into tasks._

## Workflow Mode Decision

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified:
- No coordinated schema migrations -- no new database tables are required; aggregations are computed from existing entity data.
- No breaking API changes -- the backend adds new endpoints that do not modify existing API contracts.
- No cross-cutting refactors -- changes are additive new modules and pages.
- No tightly coupled components requiring simultaneous deployment -- the backend endpoints can land first (they are additive and do not break main). The frontend dashboard page is a new route that simply will not be navigable until merged -- it does not break any existing functionality if merged after the backend.

Both repositories can receive direct-to-main PRs with task-level dependencies ensuring correct ordering (frontend tasks depend on backend tasks being completed first).

## Epic Grouping

**Strategy:** by-repository (from Hierarchy Configuration)

| Epic | Group Label | Tasks |
|---|---|---|
| TC-9006: trustify-backend | trustify-backend | Task 1, Task 2, Task 3 |
| TC-9006: trustify-ui | trustify-ui | Task 4, Task 5, Task 6 |

Documentation Task 7 is assigned to trustify-backend (API and dashboard documentation).

## Issue Type Mapping

| Role | Type Name | Hierarchy Level |
|---|---|---|
| Feature | Feature | 2 |
| Epic | Epic | 1 |
| Task | Task | 0 |

## Additional Fields (applied to all created issues)

### Epics

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

Each Epic's `parent` field is set to `TC-9006` (the Feature).

### Tasks

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

- `priority` is inherited from the parent Feature (Major). Since the Feature priority is not "Undefined", it is propagated.
- `fixVersions` is inherited from the parent Feature (RHTPA 1.5.0). No `fixVersion scope` setting exists in Jira Field Defaults, so the default scope `"both"` applies -- fixVersions are propagated to tasks.
- Each Task's `parent` field is set to its assigned Epic key.

## Issue Links

### Feature to Epics (Incorporates)

- TC-9006 **incorporates** Epic "TC-9006: trustify-backend"
- TC-9006 **incorporates** Epic "TC-9006: trustify-ui"

### Task Dependencies (Depend)

- Task 2 **depends on** Task 1
- Task 3 **depends on** Task 1
- Task 4 **depends on** Task 1
- Task 4 **depends on** Task 2
- Task 5 **depends on** Task 4
- Task 6 **depends on** Task 5
- Task 7 **depends on** Tasks 1, 2, 3, 4, 5, 6

## Documentation Signals

- **Doc impact type:** New Content
- **Details:** New documentation pages for the remediation dashboard (user guide for security teams) and aggregation endpoints (API reference for API consumers)
- **Generated:** Documentation Task 7

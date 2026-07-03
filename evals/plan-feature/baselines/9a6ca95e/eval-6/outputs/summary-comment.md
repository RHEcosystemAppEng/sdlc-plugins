# Plan Summary -- TC-9006: Add vulnerability remediation tracking dashboard

## Tasks Created

| # | Task | Repository | Parent Epic |
|---|---|---|---|
| 1 | Add remediation model types and aggregation service | trustify-backend | TC-9006: trustify-backend |
| 2 | Add remediation REST endpoints | trustify-backend | TC-9006: trustify-backend |
| 3 | Add integration tests for remediation endpoints | trustify-backend | TC-9006: trustify-backend |
| 4 | Add remediation API client functions and React Query hooks | trustify-ui | TC-9006: trustify-ui |
| 5 | Create remediation dashboard page with summary cards and progress chart | trustify-ui | TC-9006: trustify-ui |
| 6 | Add filterable vulnerability table to remediation dashboard | trustify-ui | TC-9006: trustify-ui |
| 7 | Add route and navigation for remediation dashboard | trustify-ui | TC-9006: trustify-ui |
| 8 | Document remediation dashboard and API endpoints | trustify-ui | TC-9006: trustify-ui |

## Epics Created

| Epic | Summary | Parent | Issue Type |
|---|---|---|---|
| Epic 1 | TC-9006: trustify-backend | TC-9006 | Epic (level-1) |
| Epic 2 | TC-9006: trustify-ui | TC-9006 | Epic (level-1) |

Issue Links:
- TC-9006 **incorporates** Epic 1 (TC-9006: trustify-backend)
- TC-9006 **incorporates** Epic 2 (TC-9006: trustify-ui)

## Repositories Affected

- **trustify-backend** -- new remediation module with model types, aggregation service, REST endpoints, and integration tests
- **trustify-ui** -- new remediation dashboard page with summary cards, progress chart, filterable vulnerability table, route/navigation, and API client layer

## Architecture Summary

The backend adds a new remediation sub-module under modules/fundamental/ following the existing model/service/endpoints pattern. It computes aggregated vulnerability remediation counts from existing advisory and SBOM entity data (no new database tables). Two new REST endpoints provide summary and per-product breakdowns.

The frontend adds a new RemediationDashboardPage with summary cards, a progress chart, and a filterable vulnerability table. The API layer follows the existing pattern: TypeScript interfaces in models.ts, Axios client functions in rest.ts, and React Query hooks in src/hooks/. All UI uses PatternFly 5 components.

## Inherited Field Propagation

- **Priority**: Major -- propagated to all Epics and Tasks
- **fixVersions**: RHTPA 1.5.0 -- propagated to all Epics and Tasks (fixVersion scope defaults to "both")

## Workflow Mode

direct-to-main -- no atomicity indicators identified; backend endpoints can be merged independently.

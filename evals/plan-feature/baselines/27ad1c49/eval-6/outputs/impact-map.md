# Repository Impact Map — TC-9006

## Feature

**Key**: TC-9006
**Summary**: Add vulnerability remediation tracking dashboard
**Priority**: Major
**Fix Versions**: RHTPA 1.5.0

## Epic Hierarchy

Grouping strategy: **by-repository** — one Epic per repository.

### Epics to Create

| Epic Summary | Issue Type | Parent | Repository |
|---|---|---|---|
| TC-9006: trustify-backend | Epic (level 1) | TC-9006 | trustify-backend |
| TC-9006: trustify-ui | Epic (level 1) | TC-9006 | trustify-ui |

### Incorporates Links

Links from Feature TC-9006 to each Epic (link type: Incorporates):

- TC-9006 **incorporates** Epic "TC-9006: trustify-backend"
- TC-9006 **incorporates** Epic "TC-9006: trustify-ui"

## Inherited Field Values

All Epics and Tasks inherit the following fields from Feature TC-9006:

| Field | Value |
|---|---|
| Priority | Major |
| Fix Versions | RHTPA 1.5.0 |

## Repository: trustify-backend

**Epic**: TC-9006: trustify-backend

### Changes

- New `remediation` domain module under `modules/fundamental/src/` following the existing model/service/endpoints pattern
- Model structs for remediation summary (severity x status matrix) and per-product breakdown
- Aggregation service computing remediation statistics from existing advisory and SBOM entity relationships
- Two new REST endpoints: `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`
- No new database tables — aggregations computed from existing `advisory`, `sbom_advisory`, and related entities

### Tasks

| Task | Summary | Parent Epic |
|---|---|---|
| Task 1 | Create remediation module with model structs and aggregation service | TC-9006: trustify-backend |
| Task 2 | Add remediation REST endpoints for summary and by-product breakdown | TC-9006: trustify-backend |

## Repository: trustify-ui

**Epic**: TC-9006: trustify-ui

### Changes

- TypeScript interfaces for remediation API response types in `src/api/models.ts`
- API client functions for the two remediation endpoints in `src/api/rest.ts`
- React Query hooks for remediation data fetching in `src/hooks/`
- New `RemediationDashboardPage` under `src/pages/` with summary cards, progress chart, and filterable vulnerability table
- Route registration at `/remediation` in `src/routes.tsx`
- Reuse existing `SeverityBadge` and `FilterToolbar` components

### Tasks

| Task | Summary | Parent Epic |
|---|---|---|
| Task 3 | Add remediation API types, client functions, and React Query hooks | TC-9006: trustify-ui |
| Task 4 | Build remediation dashboard page with summary cards and progress chart | TC-9006: trustify-ui |
| Task 5 | Add filterable vulnerability table to remediation dashboard | TC-9006: trustify-ui |
| Task 6 | Document remediation dashboard usage and API reference | TC-9006: trustify-ui |

## Task Dependency Ordering

```
Task 1 (backend: models + service)
  └─► Task 2 (backend: REST endpoints)
        └─► Task 3 (frontend: API client + hooks)
              └─► Task 4 (frontend: dashboard page + summary cards + chart)
                    └─► Task 5 (frontend: filterable vulnerability table)
                          └─► Task 6 (frontend: documentation)
```

Backend tasks (1-2) have lower numbers than dependent frontend tasks (3-6).

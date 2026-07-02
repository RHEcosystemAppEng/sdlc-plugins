# Repository Impact Map -- TC-9006: Add vulnerability remediation tracking dashboard

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** No atomicity constraints identified. Backend endpoints are additive (new routes, no database schema changes -- aggregations computed from existing vulnerability and SBOM relationship data). The frontend adds a new page at `/remediation` without modifying existing pages. Each PR can land independently on `main` without leaving the codebase in a broken state. No coordinated schema migrations, no breaking API changes, no cross-cutting refactors.

---

## Impact Map

```
trustify-backend:
  changes:
    - Create remediation domain models (RemediationSummary, SeverityStatusCount, RemediationTotals, ProductRemediation structs)
    - Create remediation aggregation service to compute counts from existing vulnerability and SBOM relationship data (no new database tables)
    - Add GET /api/v2/remediation/summary endpoint returning aggregated counts grouped by severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved)
    - Add GET /api/v2/remediation/by-product endpoint returning per-product remediation breakdown with total, open, in-progress, and resolved counts
    - Register remediation module routes in server/src/main.rs
    - Add integration tests for both remediation endpoints

trustify-ui:
  changes:
    - Add TypeScript interfaces for remediation API response types (RemediationSummary, ProductRemediation)
    - Add API client functions (fetchRemediationSummary, fetchRemediationByProduct) in src/api/rest.ts
    - Create React Query hooks (useRemediationSummary, useRemediationByProduct) in src/hooks/
    - Create RemediationDashboardPage with summary cards (Open, In Progress, Resolved totals) and progress chart (30-day trend)
    - Create filterable vulnerability table component with severity, product, and status filter controls
    - Register /remediation route in src/routes.tsx and add lazy-loaded page import
    - Add MSW mock handlers and fixture data for remediation endpoints
    - Add unit tests (Vitest + React Testing Library) for dashboard components
    - Add Playwright E2E test for remediation dashboard flow
```

## Epic Grouping

**Strategy:** `by-repository`

| Epic | Summary | Tasks |
|---|---|---|
| Epic 1 | TC-9006: trustify-backend | Tasks 1, 2, 3 (backend models, endpoints, tests) |
| Epic 2 | TC-9006: trustify-ui | Tasks 4, 5, 6, 7 (API layer, dashboard page, vulnerability table, routing/tests) |

## Inherited Fields

- **Priority:** Major (propagated from Feature TC-9006 to all Epics and Tasks)
- **Fix Versions:** RHTPA 1.5.0 (propagated from Feature TC-9006 to all Epics and Tasks)

# Impact Map: TC-9006 — Vulnerability Remediation Tracking Dashboard

## Feature Summary

Add a vulnerability remediation tracking dashboard that provides portfolio-wide visibility into the progress of fixing known vulnerabilities across all ingested SBOMs. The backend delivers two aggregation endpoints (`GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`), while the frontend renders a dashboard page at `/remediation` with summary cards, a progress chart, and a filterable vulnerability table.

## Workflow Mode

**Direct-to-main** — each task merges directly to `main`. The feature spans two repositories (trustify-backend and trustify-ui) with independent deployment pipelines. Direct-to-main avoids cross-repo branch coordination overhead and is appropriate because backend endpoints can be deployed before the frontend consumes them.

## Epic Hierarchy

**Grouping strategy**: by-repository (one Epic per repository)

| Epic | Issue Type | Parent | Tasks |
|---|---|---|---|
| TC-9006: trustify-backend | Epic (level 1) | TC-9006 | Tasks 1, 2, 3, 8 |
| TC-9006: trustify-ui | Epic (level 1) | TC-9006 | Tasks 4, 5, 6, 7 |

**Links**: Feature TC-9006 incorporates each Epic. Individual tasks are children of their respective Epic, not linked directly to the Feature.

## Changes by Repository

### trustify-backend

| Area | Change | Files |
|---|---|---|
| Models | New `RemediationSummary` and `ProductRemediation` response structs | `modules/fundamental/src/remediation/model/summary.rs` |
| Service | New `RemediationService` with aggregation queries against existing SBOM/advisory/vulnerability data | `modules/fundamental/src/remediation/service/remediation.rs` |
| Endpoints | `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product` | `modules/fundamental/src/remediation/endpoints/summary.rs`, `modules/fundamental/src/remediation/endpoints/by_product.rs` |
| Route registration | Mount remediation module routes | `modules/fundamental/src/remediation/endpoints/mod.rs`, `server/src/main.rs` |
| Tests | Integration tests for both endpoints | `tests/api/remediation.rs` |
| Documentation | API reference for remediation endpoints | `README.md` |

### trustify-ui

| Area | Change | Files |
|---|---|---|
| API types | `RemediationSummary`, `ProductRemediation` TypeScript interfaces | `src/api/models.ts` |
| API client | `fetchRemediationSummary()`, `fetchRemediationByProduct()` functions | `src/api/rest.ts` |
| Hooks | `useRemediationSummary`, `useRemediationByProduct` React Query hooks | `src/hooks/useRemediationSummary.ts`, `src/hooks/useRemediationByProduct.ts` |
| Dashboard page | Remediation dashboard with summary cards and progress chart | `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx`, `src/pages/RemediationDashboardPage/components/SummaryCards.tsx`, `src/pages/RemediationDashboardPage/components/ProgressChart.tsx` |
| Vulnerability table | Filterable table with severity, product, status filters | `src/pages/RemediationDashboardPage/components/VulnerabilityTable.tsx` |
| Routing | Add `/remediation` route | `src/routes.tsx` |
| Tests | Unit tests with MSW mocking, E2E test | `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx`, `tests/mocks/handlers.ts`, `tests/mocks/fixtures/remediation.json`, `tests/e2e/remediation-dashboard.spec.ts` |

## Task Dependency Graph

```
Task 1 (backend models + service)
  └─► Task 2 (backend endpoints)
        └─► Task 3 (backend integration tests)
Task 4 (frontend API client + hooks)
  └─► Task 5 (frontend dashboard page)
        └─► Task 6 (frontend vulnerability table)
              └─► Task 7 (frontend tests)
Task 8 (documentation) — depends on Task 2 and Task 6
```

## Priority and Fix Versions

- **Priority**: Major (propagated from TC-9006 to all Epics and Tasks)
- **Fix Versions**: RHTPA 1.5.0 (propagated from TC-9006 to all Epics and Tasks)

## Additional Fields

```
additional_fields: { "labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }
```

## Documentation Considerations

**Doc Impact**: New Content — the remediation dashboard and aggregation endpoints require new documentation. Task 8 covers API reference documentation for the backend endpoints.

## Non-Functional Requirements

- Summary endpoint p95 response time < 500ms (addressed via aggregation query optimization and caching in Task 2)
- Dashboard handles up to 10,000 tracked vulnerabilities (addressed via pagination in Task 6, backend query limits in Task 1)
- No new database tables — aggregations computed from existing entity relationships (enforced in Task 1)

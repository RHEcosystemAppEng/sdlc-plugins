# Impact Map: TC-9006 — Add vulnerability remediation tracking dashboard

## Feature Summary

| Field | Value |
|---|---|
| Key | TC-9006 |
| Summary | Add vulnerability remediation tracking dashboard |
| Priority | Major |
| Fix Versions | RHTPA 1.5.0 |
| Status | New |

## Workflow Mode

Direct-to-main. No atomicity constraints specified; tasks can be merged independently.

## Inherited Field Propagation

| Field | Feature Value | Propagated To | Action |
|---|---|---|---|
| Priority | Major | All Epics and Tasks | Propagated — priority is set (not Undefined) |
| Fix Versions | RHTPA 1.5.0 | All Epics and Tasks | Propagated — fixVersion scope defaults to "both" (no explicit scope config) |

## Epic Hierarchy

The project has a level-1 issue type "Epic" available. The default grouping strategy is **by-repository**. Since TC-9006 targets two repositories (trustify-backend, trustify-ui), two Epics are created.

### Epic Creation Plan

| Epic Key | Issue Type | Summary | Parent | Priority | Fix Versions |
|---|---|---|---|---|---|
| TC-9007 (simulated) | Epic | TC-9006: trustify-backend | TC-9006 | Major | RHTPA 1.5.0 |
| TC-9008 (simulated) | Epic | TC-9006: trustify-ui | TC-9006 | Major | RHTPA 1.5.0 |

**Epic TC-9007**: Backend Epic covering remediation aggregation service, REST endpoints, integration tests, and API documentation.

**Epic TC-9008**: Frontend Epic covering API client layer, dashboard page, filterable vulnerability table, and frontend tests.

### Incorporates Links

Feature TC-9006 **Incorporates** the following Epics (not individual Tasks):

| From | Link Type | To |
|---|---|---|
| TC-9006 | Incorporates | TC-9007 (TC-9006: trustify-backend) |
| TC-9006 | Incorporates | TC-9008 (TC-9006: trustify-ui) |

## Repository Impact

### trustify-backend

| Area | Change | Files |
|---|---|---|
| Remediation model | Create model types for remediation summary and per-product breakdown | `modules/fundamental/src/remediation/model/mod.rs`, `modules/fundamental/src/remediation/model/summary.rs` |
| Remediation service | Create aggregation service querying existing vulnerability and SBOM data | `modules/fundamental/src/remediation/service/mod.rs`, `modules/fundamental/src/remediation/service/remediation.rs` |
| Remediation endpoints | Create GET /api/v2/remediation/summary and GET /api/v2/remediation/by-product | `modules/fundamental/src/remediation/endpoints/mod.rs`, `modules/fundamental/src/remediation/endpoints/summary.rs`, `modules/fundamental/src/remediation/endpoints/by_product.rs` |
| Module registration | Wire remediation module into lib.rs and mount routes in server | `modules/fundamental/src/lib.rs`, `modules/fundamental/src/remediation/mod.rs`, `server/src/main.rs` |
| Integration tests | Add API integration tests for remediation endpoints | `tests/api/remediation.rs` |

### trustify-ui

| Area | Change | Files |
|---|---|---|
| API types | Add TypeScript interfaces for remediation API responses | `src/api/models.ts` |
| API client | Add client functions for remediation endpoints | `src/api/rest.ts` |
| React Query hooks | Add hooks for remediation summary and by-product data | `src/hooks/useRemediationSummary.ts`, `src/hooks/useRemediationByProduct.ts` |
| Dashboard page | Create RemediationDashboardPage with summary cards and progress chart | `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx`, `src/pages/RemediationDashboardPage/components/SummaryCards.tsx`, `src/pages/RemediationDashboardPage/components/ProgressChart.tsx` |
| Vulnerability table | Create filterable table component for outstanding vulnerabilities | `src/pages/RemediationDashboardPage/components/VulnerabilityTable.tsx` |
| Routing | Add /remediation route | `src/routes.tsx`, `src/App.tsx` |
| Tests | Add unit tests, MSW handlers, and E2E tests | `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx`, `tests/mocks/handlers.ts`, `tests/mocks/fixtures/remediation.json`, `tests/e2e/remediation-dashboard.spec.ts` |

## Task Plan

| Task | Slug | Repository | Parent Epic | Priority | Fix Versions | Dependencies |
|---|---|---|---|---|---|---|
| 1 | remediation-model-service | trustify-backend | TC-9007 | Major | RHTPA 1.5.0 | None |
| 2 | remediation-endpoints | trustify-backend | TC-9007 | Major | RHTPA 1.5.0 | Task 1 |
| 3 | remediation-integration-tests | trustify-backend | TC-9007 | Major | RHTPA 1.5.0 | Task 2 |
| 4 | remediation-api-client-hooks | trustify-ui | TC-9008 | Major | RHTPA 1.5.0 | Task 2 |
| 5 | remediation-dashboard-page | trustify-ui | TC-9008 | Major | RHTPA 1.5.0 | Task 4 |
| 6 | vulnerability-table | trustify-ui | TC-9008 | Major | RHTPA 1.5.0 | Task 5 |
| 7 | remediation-documentation | trustify-backend | TC-9007 | Major | RHTPA 1.5.0 | Task 3, Task 6 |

## Documentation Impact

The feature specifies "New Content" documentation considerations. Task 7 is a documentation task covering both the remediation dashboard user guide and API endpoint reference. It is assigned to the backend Epic since the primary documentation deliverable is the REST API reference.

## Non-MVP Items (Excluded from Plan)

- **Export remediation report as CSV**: Marked as non-MVP in the feature requirements. Excluded from this plan.

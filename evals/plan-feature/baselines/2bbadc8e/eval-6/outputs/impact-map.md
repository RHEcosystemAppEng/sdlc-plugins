# Repository Impact Map — TC-9006

## Workflow Mode

**Mode:** direct-to-main
**Rationale:** No atomicity indicators identified. The backend endpoints are purely additive — merging them into main without the frontend does not break existing functionality. The frontend tasks depend on backend tasks being merged first, but dependency ordering within direct-to-main mode handles this. No coordinated schema migrations are required (the feature explicitly states no new database tables). No breaking API changes — the endpoints are net-new.

## Epic Hierarchy

A level-1 issue type (Epic) is available. Grouping strategy: **by-repository**.

| Epic | Summary | Parent |
|---|---|---|
| Epic 1 | TC-9006: trustify-backend | TC-9006 |
| Epic 2 | TC-9006: trustify-ui | TC-9006 |

**Incorporates links:** Feature TC-9006 -> Epic 1, Feature TC-9006 -> Epic 2
(Feature links to Epics, not to individual Tasks.)

## trustify-backend

Epic: TC-9006: trustify-backend

Changes:
- Add remediation model structs (RemediationSummary, ProductRemediation) following the existing model/ pattern
- Add RemediationService with aggregation queries against existing vulnerability and SBOM relationship data (no new tables)
- Add GET /api/v2/remediation/summary endpoint returning aggregated counts by severity and status
- Add GET /api/v2/remediation/by-product endpoint returning per-product remediation breakdown
- Register remediation routes in server/main.rs
- Add integration tests for both remediation endpoints

## trustify-ui

Epic: TC-9006: trustify-ui

Changes:
- Add TypeScript interfaces for remediation API response types
- Add API client functions for remediation endpoints
- Add React Query hooks for remediation data fetching
- Add RemediationDashboardPage with summary cards (Open, In Progress, Resolved counts)
- Add progress chart showing remediation trend over time
- Add filterable vulnerability table with severity, product, and status filters
- Register /remediation route in routes.tsx
- Add MSW mock handlers and test fixtures for remediation endpoints
- Add unit tests for remediation dashboard page

## Excluded Requirements

| Requirement | Reason |
|---|---|
| Export remediation report as CSV | Marked as non-MVP in the feature description. Can be planned as a follow-up after the dashboard is delivered. |

## Task-to-Epic Assignment

| Task | Repository | Epic |
|---|---|---|
| Task 1: Add remediation model and aggregation service | trustify-backend | TC-9006: trustify-backend |
| Task 2: Add remediation API endpoints | trustify-backend | TC-9006: trustify-backend |
| Task 3: Add remediation endpoint integration tests | trustify-backend | TC-9006: trustify-backend |
| Task 4: Add remediation API client and React Query hooks | trustify-ui | TC-9006: trustify-ui |
| Task 5: Add remediation dashboard page with summary cards and progress chart | trustify-ui | TC-9006: trustify-ui |
| Task 6: Add filterable vulnerability table to remediation dashboard | trustify-ui | TC-9006: trustify-ui |
| Task 7: Add remediation dashboard tests | trustify-ui | TC-9006: trustify-ui |
| Task 8: Add remediation feature documentation | trustify-backend | TC-9006: trustify-backend |

## Dependencies

```
Task 1 (model/service) -> Task 2 (endpoints) -> Task 3 (tests)
Task 2 (endpoints) -> Task 4 (API client/hooks) -> Task 5 (dashboard page) -> Task 6 (table)
Task 5, Task 6 -> Task 7 (dashboard tests)
Task 1-7 -> Task 8 (documentation)
```

# Repository Impact Map — TC-9006: Add vulnerability remediation tracking dashboard

## trustify-backend

changes:
  - Add remediation aggregation model structs (RemediationSummary with severity-by-status breakdown, ProductRemediation with per-product counts)
  - Add remediation aggregation service computing summaries from existing vulnerability/SBOM data (no new database tables)
  - Add GET /api/v2/remediation/summary endpoint returning overall severity-by-status aggregation
  - Add GET /api/v2/remediation/by-product endpoint returning per-product remediation breakdown with pagination
  - Add integration tests for remediation endpoints covering normal, empty, large-dataset, and pagination scenarios

## trustify-ui

changes:
  - Add TypeScript interfaces for remediation API response shapes (RemediationSummary, SeverityBreakdown, ProductRemediation)
  - Add API client functions (fetchRemediationSummary, fetchRemediationByProduct) using the shared Axios instance
  - Add React Query hooks (useRemediationSummary, useRemediationByProduct) for data fetching
  - Add RemediationDashboardPage at /remediation with summary cards, progress chart, and filterable vulnerability table
  - Add route definition for /remediation with lazy loading
  - Add MSW mock handlers and fixture data for remediation endpoints
  - Add Playwright E2E test for the remediation dashboard

## Excluded Requirements

- **Export remediation report as CSV** — This is marked as non-MVP in the feature requirements. It can be planned as a follow-up feature once the core dashboard is implemented. No design mockups or detailed specification for the export format are available.

---

## Workflow Mode

**Selected mode:** `feature-branch`

**Rationale:** Atomicity indicator #4 (tightly coupled feature components) applies. The frontend remediation dashboard page requires the new backend `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product` endpoints, which do not yet exist. Merging only the frontend would produce a non-functional page calling missing endpoints; merging only the backend provides no user-facing value. Both sides must land together for the feature to function.

**Interdependent tasks:** All backend implementation tasks (2-5) and frontend implementation tasks (6-8) are interdependent. Frontend tasks 6-8 depend on the backend endpoints defined in Tasks 3-4. The merge-branch task (10) depends on all intermediate tasks.

Note: The `workflow:feature-branch` label will be applied to the TC-9006 feature issue in Step 6a.

---

## Epic Hierarchy

### Issue Type Discovery (Step 2.5)

Type-to-role mapping:
  Feature: Feature (level: 2)
  Epic:    Epic (level: 1)
  Task:    Task (level: 0)

### Epic Grouping Strategy

Strategy: `by-repository` (from CLAUDE.md Hierarchy Configuration default)

### Epics Created

**Epic 1: TC-9006: trustify-backend**
- Issue type: Epic (hierarchyLevel 1)
- Parent: TC-9006 (Feature)
- Description: Backend implementation for the vulnerability remediation tracking dashboard. Includes remediation aggregation model structs, service logic, REST endpoints, integration tests, documentation, and feature-branch bookend tasks.
- additional_fields: `{ "labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }`
- Tasks: 1 (create-branch), 2, 3, 4, 5, 9 (documentation), 10 (merge-branch)

**Epic 2: TC-9006: trustify-ui**
- Issue type: Epic (hierarchyLevel 1)
- Parent: TC-9006 (Feature)
- Description: Frontend implementation for the vulnerability remediation tracking dashboard. Includes TypeScript API layer, React Query hooks, dashboard page with summary cards, progress chart, filterable table, MSW mocks, and E2E tests.
- additional_fields: `{ "labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }`
- Tasks: 6, 7, 8

### Incorporates Links

- TC-9006 (Feature) **Incorporates** Epic "TC-9006: trustify-backend"
- TC-9006 (Feature) **Incorporates** Epic "TC-9006: trustify-ui"

Note: Incorporates links go from Feature to each Epic, NOT from Feature to individual Tasks. Tasks inherit hierarchy through their Epic parent.

---

## Task Creation Log

All tasks created with:
- `labels`: `["ai-generated-jira"]`
- `priority`: `{"name": "Major"}` (inherited from Feature TC-9006, priority is "Major" — not "Undefined", so it is propagated)
- `fixVersions`: `[{"name": "RHTPA 1.5.0"}]` (inherited from Feature TC-9006; fixVersion scope is absent from Jira Field Defaults, defaulting to "both" — propagated to tasks)

| Task | Summary | Repository | Epic | Target Branch |
|---|---|---|---|---|
| 1 | Create feature branch TC-9006 from main | trustify-backend | TC-9006: trustify-backend | main |
| 2 | Add remediation aggregation model structs | trustify-backend | TC-9006: trustify-backend | TC-9006 |
| 3 | Add remediation aggregation service | trustify-backend | TC-9006: trustify-backend | TC-9006 |
| 4 | Add remediation summary and by-product endpoints | trustify-backend | TC-9006: trustify-backend | TC-9006 |
| 5 | Add remediation endpoint integration tests | trustify-backend | TC-9006: trustify-backend | TC-9006 |
| 6 | Add remediation API layer (types, client, hooks) | trustify-ui | TC-9006: trustify-ui | TC-9006 |
| 7 | Add remediation dashboard page with summary cards, chart, and filterable table | trustify-ui | TC-9006: trustify-ui | TC-9006 |
| 8 | Add MSW mocks, fixtures, and E2E test for remediation dashboard | trustify-ui | TC-9006: trustify-ui | TC-9006 |
| 9 | Documentation: remediation dashboard and aggregation endpoints | trustify-backend | TC-9006: trustify-backend | TC-9006 |
| 10 | Merge feature branch TC-9006 to main | trustify-backend | TC-9006: trustify-backend | main |

## Documentation Signals

- **Doc impact type**: New Content
- **Details**: Document the remediation dashboard and aggregation endpoints. Security teams need a guide for using the dashboard; API consumers need endpoint reference.
- **Generated**: Task 9 (documentation task)

## Inherited Field Propagation Summary

- **Priority**: "Major" (from Feature TC-9006) — propagated to all created tasks and Epics
- **fixVersions**: ["RHTPA 1.5.0"] (from Feature TC-9006) — propagated to all created tasks and Epics (fixVersion scope absent from Jira Field Defaults, defaults to "both")

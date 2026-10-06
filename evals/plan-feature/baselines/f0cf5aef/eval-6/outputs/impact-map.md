# Repository Impact Map — TC-9006: Add vulnerability remediation tracking dashboard

## trustify-backend

Changes:
- Add `remediation` module under `modules/fundamental/src/` following the existing `model/ + service/ + endpoints/` pattern
- Implement `GET /api/v2/remediation/summary` endpoint returning aggregated vulnerability counts grouped by severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved)
- Implement `GET /api/v2/remediation/by-product` endpoint returning per-product remediation breakdown with total, open, and resolved counts per product
- Implement `GET /api/v2/remediation/export` endpoint returning a CSV file of the remediation report for management reporting
- Add integration tests for all remediation endpoints in `tests/api/remediation.rs`
- Register remediation module routes in `server/src/main.rs`

## trustify-ui

Changes:
- Add TypeScript interfaces for remediation API response types in `src/api/models.ts`
- Add API client functions for remediation endpoints in `src/api/rest.ts`
- Add React Query hooks for remediation data fetching in `src/hooks/`
- Add `RemediationDashboardPage` at `/remediation` route with summary cards (total Open, In Progress, Resolved) and a progress chart showing remediation trend over the past 30 days
- Add filterable vulnerability table component with severity, product, and status filter controls using PatternFly FilterToolbar
- Add CSV export button triggering file download from the backend export endpoint
- Register `/remediation` route in `src/routes.tsx`
- Add unit tests with MSW handlers and mock fixtures for remediation page and components
- Add Playwright E2E test for remediation dashboard navigation and filtering

## Epic Grouping (by-repository)

- **Epic: TC-9006: trustify-backend** — Backend aggregation service, REST endpoints, and integration tests for remediation tracking
- **Epic: TC-9006: trustify-ui** — Frontend dashboard page, components, API client, hooks, and tests for remediation tracking

## Workflow Mode

**Selected mode: `feature-branch`**

**Rationale:** Atomicity indicator #4 (Tightly coupled feature components) is present. The frontend dashboard page requires backend API endpoints (`/api/v2/remediation/summary`, `/api/v2/remediation/by-product`, `/api/v2/remediation/export`) that do not yet exist. Merging the frontend without the backend would result in a broken dashboard page with failing API calls. Merging the backend without the frontend provides no user-facing value but is not broken. The interdependency is structural: frontend tasks depend on backend tasks for their API contracts.

**Interdependent tasks:**
- Frontend API client/hooks tasks depend on backend endpoint tasks for request/response shapes
- Frontend dashboard page depends on API client/hooks
- Frontend filterable table depends on API client/hooks
- Frontend CSV export button depends on backend CSV export endpoint

The `workflow:feature-branch` label will be applied to the feature issue TC-9006.

## Excluded Requirements

None. All requirements (MVP and non-MVP) from the feature description are covered by the planned tasks.

## additional_fields for Created Issues

All created Epics and Tasks will include:
- `labels`: `["ai-generated-jira"]`
- `priority`: `{"name": "Major"}` (inherited from Feature TC-9006)
- `fixVersions`: `[{"name": "RHTPA 1.5.0"}]` (inherited from Feature TC-9006; fixVersion scope defaults to "both" since no Jira Field Defaults section is configured)

Epics will additionally have:
- `parent`: `{"key": "TC-9006"}` (Feature as parent)

Tasks will additionally have:
- `parent`: `{"key": "<epic-key>"}` (assigned Epic as parent, determined after Epic creation)

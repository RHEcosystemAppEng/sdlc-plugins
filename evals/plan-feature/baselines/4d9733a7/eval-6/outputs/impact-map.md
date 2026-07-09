# Repository Impact Map

**Feature:** TC-9006 — Add vulnerability remediation tracking dashboard
**Priority:** Major
**Fix Versions:** RHTPA 1.5.0

## Epic Hierarchy

Grouping strategy: **by-repository**
Level-1 issue type: **Epic**

| Epic | Summary | Parent | Issue Type |
|---|---|---|---|
| Epic 1 | TC-9006: trustify-backend | TC-9006 | Epic |
| Epic 2 | TC-9006: trustify-ui | TC-9006 | Epic |

**Incorporates links:** Feature TC-9006 incorporates Epic 1 and Epic 2 (not individual Tasks).

## trustify-backend

Epic: **TC-9006: trustify-backend**

Changes:
- Create a new `remediation` module under `modules/fundamental/src/` following the established model/service/endpoints pattern
- Implement `GET /api/v2/remediation/summary` endpoint returning aggregated vulnerability counts by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved)
- Implement `GET /api/v2/remediation/by-product` endpoint returning per-product remediation breakdown with total, open, and resolved counts
- Register remediation routes in `server/src/main.rs`
- Add integration tests for both remediation endpoints in `tests/api/`

## trustify-ui

Epic: **TC-9006: trustify-ui**

Changes:
- Add TypeScript interfaces for remediation API response types in `src/api/models.ts`
- Add API client functions for remediation endpoints in `src/api/rest.ts`
- Add React Query hooks for remediation data fetching in `src/hooks/`
- Create a new `RemediationDashboard` page under `src/pages/` with summary cards, a progress chart, and a filterable vulnerability table
- Register the `/remediation` route in `src/routes.tsx`
- Add unit tests with React Testing Library and MSW mock handlers for the remediation dashboard

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present:
- No coordinated schema migrations (the feature explicitly requires no new database tables)
- No breaking API changes (all endpoints are new additions, not modifications to existing contracts)
- No cross-cutting refactors
- No tightly coupled components requiring simultaneous deployment (backend endpoints can be merged and deployed first; the frontend page adds a new route at `/remediation` that does not affect existing routes or functionality)

Backend tasks can merge independently to `main` before frontend tasks. The natural task ordering (backend first, frontend second) ensures endpoints exist before the UI calls them.

## Excluded Requirements

| Requirement | Reason |
|---|---|
| Export remediation report as CSV | Non-MVP requirement per feature specification. Can be planned in a subsequent iteration once the core dashboard is delivered. |

## Epic Creation Details

Each Epic is created with:
- Issue type: `Epic` (hierarchyLevel 1)
- Parent: `TC-9006`
- Labels: `["ai-generated-jira"]`
- Priority: `{"name": "Major"}` (inherited from Feature)
- Fix Versions: `[{"name": "RHTPA 1.5.0"}]` (inherited from Feature; fixVersion scope defaults to "both")

## Task-to-Epic Assignment

| Task | Epic |
|---|---|
| Task 1: Create remediation module with summary endpoint | TC-9006: trustify-backend |
| Task 2: Add remediation by-product endpoint | TC-9006: trustify-backend |
| Task 3: Add integration tests for remediation endpoints | TC-9006: trustify-backend |
| Task 4: Add remediation API types, client functions, and React Query hooks | TC-9006: trustify-ui |
| Task 5: Create remediation dashboard page with summary cards and progress chart | TC-9006: trustify-ui |
| Task 6: Add filterable vulnerability table to remediation dashboard | TC-9006: trustify-ui |
| Task 7: Add tests for remediation dashboard | TC-9006: trustify-ui |
| Task 8: Document remediation dashboard and aggregation API endpoints | TC-9006: trustify-ui |

# Repository Impact Map — TC-9006

## Feature: Add vulnerability remediation tracking dashboard

## Epic Grouping Strategy: by-repository

### Epics

| Epic | Summary | Issue Type | Parent | Repository |
|------|---------|------------|--------|------------|
| Epic 1 | TC-9006: trustify-backend | Epic (level 1) | TC-9006 | trustify-backend |
| Epic 2 | TC-9006: trustify-ui | Epic (level 1) | TC-9006 | trustify-ui |

Epic creation uses the level-1 issue type named 'Epic' with `parent` set to the feature issue key `TC-9006`.

### Epic Issue Creation Details

Each Epic is created with:
- `issueTypeName`: Epic
- `parent`: TC-9006 (feature issue key)
- `labels`: ["ai-generated-jira"]
- `priority`: {"name": "Major"} (inherited from Feature TC-9006)
- `fixVersions`: [{"name": "RHTPA 1.5.0"}] (inherited from Feature TC-9006)

### Incorporates Links

- TC-9006 **Incorporates** Epic 1 (TC-9006: trustify-backend)
- TC-9006 **Incorporates** Epic 2 (TC-9006: trustify-ui)

Note: Incorporates links go from the Feature to Epics, not from the Feature to individual Tasks. Tasks inherit hierarchy through their Epic parent.

---

## trustify-backend

Parent Epic: TC-9006: trustify-backend

changes:
  - Create remediation domain module with model structs for summary and per-product aggregation response types
  - Implement RemediationService with aggregation queries against existing vulnerability and SBOM relationship tables
  - Add GET /api/v2/remediation/summary endpoint returning counts by severity x status
  - Add GET /api/v2/remediation/by-product endpoint returning per-product remediation breakdown
  - Mount remediation routes in server/src/main.rs
  - Add integration tests for both remediation endpoints in tests/api/
  - Document the new aggregation API endpoints

Tasks: 1, 2, 3, 9 (documentation)

---

## trustify-ui

Parent Epic: TC-9006: trustify-ui

changes:
  - Add TypeScript interfaces for remediation API response types in api/models.ts
  - Add API client functions for remediation endpoints in api/rest.ts
  - Create React Query hooks for remediation summary and by-product data
  - Create RemediationDashboardPage with summary cards (Open, In Progress, Resolved counts)
  - Add progress chart showing remediation trend over the past 30 days
  - Add filterable vulnerability table with severity, product, and status filters
  - Register /remediation route in routes.tsx and add navigation entry
  - Add unit tests, MSW mock handlers, and Playwright E2E tests for the dashboard

Tasks: 4, 5, 6, 7, 8

---

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified that would require all changes to land together:
1. No coordinated schema migrations — the feature explicitly states "No new database tables" and computes aggregations from existing data.
2. No breaking API changes — all endpoints are new additions (`/api/v2/remediation/summary`, `/api/v2/remediation/by-product`); no existing endpoints are modified.
3. No cross-cutting refactors — changes are additive in both repositories.
4. Components are not tightly coupled for deployment — backend endpoints are additive and can land independently without breaking existing functionality. Frontend pages are new routes that do not modify existing pages. Task ordering (backend before frontend) ensures endpoints exist before the UI depends on them.

Each PR independently leaves `main` in a working state. Backend PRs add new endpoints; frontend PRs add new pages.

---

## Excluded Requirements

| Requirement | Reason |
|---|---|
| Export remediation report as CSV | Marked as non-MVP in feature requirements. Can be planned in a follow-up iteration once the core dashboard is delivered. |

---

## Field Inheritance

- **Priority**: Major (inherited from Feature TC-9006, propagated to all Epics and Tasks)
- **fixVersions**: RHTPA 1.5.0 (inherited from Feature TC-9006, propagated to all Epics and Tasks; fixVersion scope defaults to "both" as no Jira Field Defaults section exists in CLAUDE.md)

---

## Task Summary

| Task # | Summary | Repository | Parent Epic |
|--------|---------|------------|-------------|
| 1 | Create remediation domain models and aggregation service | trustify-backend | TC-9006: trustify-backend |
| 2 | Add remediation REST endpoints with route registration | trustify-backend | TC-9006: trustify-backend |
| 3 | Add integration tests for remediation endpoints | trustify-backend | TC-9006: trustify-backend |
| 4 | Add remediation API types, client functions, and React Query hooks | trustify-ui | TC-9006: trustify-ui |
| 5 | Create remediation dashboard page with summary cards and progress chart | trustify-ui | TC-9006: trustify-ui |
| 6 | Add filterable vulnerability table to remediation dashboard | trustify-ui | TC-9006: trustify-ui |
| 7 | Register remediation dashboard route and add navigation entry | trustify-ui | TC-9006: trustify-ui |
| 8 | Add unit and E2E tests for remediation dashboard | trustify-ui | TC-9006: trustify-ui |
| 9 | Document remediation dashboard and aggregation API endpoints | trustify-backend | TC-9006: trustify-backend |

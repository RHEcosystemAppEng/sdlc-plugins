# Repository Impact Map — TC-9006: Add vulnerability remediation tracking dashboard

## Epic Grouping Strategy

**Strategy:** by-repository (from CLAUDE.md Hierarchy Configuration)

Two Epics are created between the Feature (TC-9006) and the implementation Tasks:

| Epic | Summary | Issue Type | Parent | Labels | Priority | Fix Versions |
|---|---|---|---|---|---|---|
| Epic 1 | TC-9006: trustify-backend | Epic (level 1) | TC-9006 | ai-generated-jira | Major | RHTPA 1.5.0 |
| Epic 2 | TC-9006: trustify-ui | Epic (level 1) | TC-9006 | ai-generated-jira | Major | RHTPA 1.5.0 |

### Epic Creation Parameters

Each Epic is created with:
- `issueTypeName`: Epic
- `parent`: TC-9006 (the Feature issue key)
- `additional_fields`:
  - `labels`: ["ai-generated-jira"]
  - `priority`: {"name": "Major"}
  - `fixVersions`: [{"name": "RHTPA 1.5.0"}]

## Incorporates Link Structure

Links are created from the **Feature to each Epic** (not from Feature to individual Tasks):

- TC-9006 **Incorporates** Epic 1 (TC-9006: trustify-backend)
- TC-9006 **Incorporates** Epic 2 (TC-9006: trustify-ui)

Tasks inherit hierarchy through their Epic parent field, not through direct Feature links.

## Workflow Mode

**Selected mode:** direct-to-main

**Rationale:** No atomicity indicators identified:
- No coordinated schema migrations — the feature explicitly states "No new database tables"
- No breaking API changes — all endpoints are new additions (`/api/v2/remediation/summary`, `/api/v2/remediation/by-product`)
- No cross-cutting refactors — changes are additive
- Not tightly coupled for merge purposes — backend endpoints can merge first (they are additive and do not break existing behavior), then frontend can merge after backend is available

Backend tasks merge to main first, then frontend tasks merge to main once backend endpoints are available.

## Repository Impact Map

### trustify-backend

**Epic:** TC-9006: trustify-backend

Changes:
- Add remediation model types (RemediationSummary, SeverityStatusCount, ProductRemediation) in a new remediation module
- Add RemediationService with aggregation queries against existing vulnerability and SBOM relationship data
- Add GET /api/v2/remediation/summary endpoint returning aggregated counts by severity and status
- Add GET /api/v2/remediation/by-product endpoint returning per-product remediation breakdown
- Register remediation module routes in server main
- Add integration tests for both remediation endpoints

### trustify-ui

**Epic:** TC-9006: trustify-ui

Changes:
- Add TypeScript interfaces for remediation API response types
- Add API client functions for remediation endpoints
- Add React Query hooks for remediation data fetching
- Add RemediationDashboardPage with summary cards (Open, In Progress, Resolved) and progress chart (30-day trend)
- Add filterable vulnerability table component with severity, product, and status filters
- Register /remediation route and add navigation link

## Task-to-Epic Assignment

| Task | Repository | Epic |
|---|---|---|
| Task 1 — Add remediation model types and aggregation service | trustify-backend | TC-9006: trustify-backend |
| Task 2 — Add remediation REST endpoints | trustify-backend | TC-9006: trustify-backend |
| Task 3 — Add integration tests for remediation endpoints | trustify-backend | TC-9006: trustify-backend |
| Task 4 — Add remediation API types, client functions, and React Query hooks | trustify-ui | TC-9006: trustify-ui |
| Task 5 — Add remediation dashboard page with summary cards and progress chart | trustify-ui | TC-9006: trustify-ui |
| Task 6 — Add filterable vulnerability table to remediation dashboard | trustify-ui | TC-9006: trustify-ui |
| Task 7 — Document remediation dashboard and API endpoints | trustify-backend | TC-9006: trustify-backend |

## Excluded Requirements

| Requirement | Reason for Exclusion |
|---|---|
| Export remediation report as CSV | Marked as non-MVP in the Feature requirements. Can be planned in a follow-up iteration once the core dashboard and endpoints are delivered. |

## Field Inheritance

- **Priority:** Major (inherited from TC-9006, propagated to all Epics and Tasks)
- **Fix Versions:** RHTPA 1.5.0 (inherited from TC-9006, propagated to all Epics and Tasks; fixVersion scope defaults to "both" since no Jira Field Defaults section is configured)

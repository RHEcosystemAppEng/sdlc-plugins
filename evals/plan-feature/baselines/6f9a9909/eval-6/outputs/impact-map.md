# Repository Impact Map -- TC-9006

**Feature:** Add vulnerability remediation tracking dashboard
**Priority:** Major
**Fix Versions:** RHTPA 1.5.0

---

## Epic Hierarchy

**Grouping strategy:** by-repository (from CLAUDE.md Hierarchy Configuration)
**Issue type:** Epic (hierarchyLevel 1)

### Epic Creation Parameters

Each Epic is created with:
- **Issue type:** Epic (level-1 issue type, hierarchyLevel 1)
- **Parent:** TC-9006 (the Feature issue)
- **Labels:** `["ai-generated-jira"]`
- **Priority:** Major (inherited from Feature TC-9006)
- **fixVersions:** `[{"name": "RHTPA 1.5.0"}]` (inherited from Feature TC-9006; no `fixVersion scope` setting in Jira Field Defaults -- default "both" applies, so propagated to Epics and Tasks)

| Epic Key | Summary | Parent | Type | Priority | fixVersions |
|---|---|---|---|---|---|
| TC-9007 | TC-9006: trustify-backend | TC-9006 | Epic | Major | RHTPA 1.5.0 |
| TC-9008 | TC-9006: trustify-ui | TC-9006 | Epic | Major | RHTPA 1.5.0 |

### Epic Descriptions

**TC-9007 -- TC-9006: trustify-backend**
Backend implementation for the vulnerability remediation tracking dashboard. Adds a remediation module with data models, aggregation service, and two REST endpoints for remediation summary and per-product breakdown. Includes integration tests for the new endpoints.

**TC-9008 -- TC-9006: trustify-ui**
Frontend implementation for the vulnerability remediation tracking dashboard. Adds API client layer, React Query hooks, the remediation dashboard page with summary cards, progress chart, and filterable vulnerability table. Includes unit and component tests.

### Incorporates Links

Links are created from the **Feature** to each **Epic** (not to individual Tasks):
- TC-9006 **incorporates** TC-9007 (trustify-backend Epic)
- TC-9006 **incorporates** TC-9008 (trustify-ui Epic)

---

## trustify-backend

Changes:
- Add remediation module under `modules/fundamental/src/remediation/` with model structs for remediation summary and by-product responses
- Add aggregation service to compute remediation status from existing vulnerability and SBOM relationship data (no new database tables per NFR)
- Add `GET /api/v2/remediation/summary` endpoint returning aggregated counts by severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved)
- Add `GET /api/v2/remediation/by-product` endpoint returning per-product remediation breakdown with total, open, and resolved counts
- Register remediation module routes in `server/src/main.rs`
- Add integration tests for both remediation endpoints in `tests/api/`

Tasks assigned to Epic TC-9007:

| Task # | Summary |
|---|---|
| 1 | Add remediation data models and aggregation service |
| 2 | Add remediation summary endpoint |
| 3 | Add remediation by-product endpoint |
| 4 | Add integration tests for remediation endpoints |
| 9 | Document remediation dashboard and API endpoints |

---

## trustify-ui

Changes:
- Add TypeScript interfaces for remediation API response types in `src/api/models.ts`
- Add API client functions for remediation endpoints in `src/api/rest.ts`
- Add React Query hooks for remediation summary and by-product data
- Add `RemediationDashboardPage` at `/remediation` with summary cards (total open, in-progress, resolved) and progress chart (trend over 30 days)
- Register the remediation dashboard route in `src/routes.tsx`
- Add filterable vulnerability table with severity, product, and status filters using PatternFly FilterToolbar
- Add unit tests with Vitest + React Testing Library and MSW handlers for remediation endpoints

Tasks assigned to Epic TC-9008:

| Task # | Summary |
|---|---|
| 5 | Add API client and React Query hooks for remediation endpoints |
| 6 | Add remediation dashboard page with summary cards and progress chart |
| 7 | Add filterable vulnerability table to remediation dashboard |
| 8 | Add tests for remediation dashboard page |

---

## Workflow Mode

**Selected mode:** direct-to-main

**Rationale:** No atomicity indicators were identified:
1. **No coordinated schema migrations** -- no new database tables; aggregations are computed from existing vulnerability and SBOM relationship data.
2. **No breaking API changes** -- all endpoints are new and additive; no existing endpoints are modified.
3. **No cross-cutting refactors** -- changes are isolated to new modules in each repository.
4. **No tightly coupled cross-repo delivery** -- backend and frontend are in separate repositories. Backend endpoints are additive and non-breaking. Task dependency ordering (backend tasks 1-4 before frontend tasks 5-8) ensures endpoints exist before the frontend consumes them.

---

## Priority and fixVersion Inheritance

- **Priority:** Major -- inherited from Feature TC-9006, propagated to all Epics and Tasks via `additional_fields.priority`.
- **fixVersions:** RHTPA 1.5.0 -- inherited from Feature TC-9006. No `fixVersion scope` setting found in Jira Field Defaults (default: "both"), so propagated to all Epics and Tasks via `additional_fields.fixVersions`.

### additional_fields for all created issues

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

---

## Documentation Signals

- **Doc impact type:** New Content
- **Details:** Document the remediation dashboard and aggregation endpoints. Security teams need a guide for using the dashboard; API consumers need endpoint reference.
- Documentation task (Task 9) generated and assigned to trustify-backend Epic (TC-9007).

---

## Deferred Requirements (non-MVP)

- **Export remediation report as CSV** -- explicitly marked as non-MVP in the Feature description. Can be planned as a follow-up once the core dashboard is delivered. No missing inputs prevent planning; deferral is a scope decision.

---

## Task-to-Epic Assignment

| Task # | Summary | Repository | Parent Epic |
|---|---|---|---|
| 1 | Add remediation data models and aggregation service | trustify-backend | TC-9007 |
| 2 | Add remediation summary endpoint | trustify-backend | TC-9007 |
| 3 | Add remediation by-product endpoint | trustify-backend | TC-9007 |
| 4 | Add integration tests for remediation endpoints | trustify-backend | TC-9007 |
| 5 | Add API client and React Query hooks for remediation endpoints | trustify-ui | TC-9008 |
| 6 | Add remediation dashboard page with summary cards and progress chart | trustify-ui | TC-9008 |
| 7 | Add filterable vulnerability table to remediation dashboard | trustify-ui | TC-9008 |
| 8 | Add tests for remediation dashboard page | trustify-ui | TC-9008 |
| 9 | Document remediation dashboard and API endpoints | trustify-backend | TC-9007 |

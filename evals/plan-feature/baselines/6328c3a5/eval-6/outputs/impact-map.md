# Repository Impact Map — TC-9006: Add vulnerability remediation tracking dashboard

## Epic Hierarchy

**Grouping strategy:** by-repository

### Epic 1: TC-9006: trustify-backend
- **Issue type:** Epic (level-1)
- **Parent:** TC-9006 (Feature)
- **Summary:** TC-9006: trustify-backend
- **Description:** Backend remediation aggregation service and REST endpoints for vulnerability remediation tracking. Covers model types, service layer, endpoint registration, and integration tests.
- **additional_fields:**
  - `labels`: ["ai-generated-jira"]
  - `priority`: {"name": "Major"}
  - `fixVersions`: [{"name": "RHTPA 1.5.0"}]

### Epic 2: TC-9006: trustify-ui
- **Issue type:** Epic (level-1)
- **Parent:** TC-9006 (Feature)
- **Summary:** TC-9006: trustify-ui
- **Description:** Frontend remediation dashboard page with summary cards, progress chart, filterable vulnerability table, API client layer, and component tests.
- **additional_fields:**
  - `labels`: ["ai-generated-jira"]
  - `priority`: {"name": "Major"}
  - `fixVersions`: [{"name": "RHTPA 1.5.0"}]

### Issue Links

- **Feature TC-9006** → Incorporates → Epic "TC-9006: trustify-backend"
- **Feature TC-9006** → Incorporates → Epic "TC-9006: trustify-ui"

(Feature links to Epics only, not to individual Tasks. Tasks inherit hierarchy through their Epic parent.)

---

## Workflow Mode

**Selected mode:** direct-to-main

**Rationale:** No atomicity indicators identified:
- No coordinated schema migrations — no new database tables are required; aggregations are computed from existing vulnerability and SBOM relationship data.
- No breaking API changes — both endpoints (`/api/v2/remediation/summary` and `/api/v2/remediation/by-product`) are new additions, not modifications to existing contracts.
- No cross-cutting refactors — the remediation module is self-contained within the backend, and the frontend dashboard is a new page.
- Not tightly coupled for deployment — backend endpoints can land on main independently (they are additive, unused until the frontend integrates them). Frontend tasks depend on backend being available but do not require coordinated deployment.

---

## Impact Map

### trustify-backend
**changes:**
- Create remediation module with model types (`RemediationSummary`, `SeverityStatusCount`, `ProductRemediation`) and service layer for computing aggregations from existing vulnerability-SBOM join data
- Add `GET /api/v2/remediation/summary` endpoint returning aggregated counts grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved)
- Add `GET /api/v2/remediation/by-product` endpoint returning per-product remediation breakdown with total, open, and resolved counts
- Register remediation routes in the Axum server route tree
- Add integration tests for both remediation endpoints in `tests/api/`

### trustify-ui
**changes:**
- Add TypeScript interfaces for remediation API response types (`RemediationSummary`, `ProductRemediation`, `VulnerabilityItem`)
- Add API client functions (`fetchRemediationSummary`, `fetchRemediationByProduct`) in the REST client layer
- Create React Query hooks (`useRemediationSummary`, `useRemediationByProduct`) for data fetching
- Create `RemediationDashboardPage` with summary cards (Open, In Progress, Resolved counts) and progress chart (trend over 30 days)
- Add `/remediation` route definition and navigation entry
- Create filterable `VulnerabilityTable` component with severity, product, and status filter controls
- Add unit tests for dashboard components with MSW mock handlers and fixture data

### Deferred (non-MVP)
- **CSV export** — "Export remediation report as CSV" is marked non-MVP in the feature requirements. This can be planned in a follow-up iteration once the core dashboard is delivered.

---

## Task-to-Epic Assignment

| Task | Summary | Repository | Epic |
|---|---|---|---|
| Task 1 | Create remediation model and service layer | trustify-backend | TC-9006: trustify-backend |
| Task 2 | Add remediation REST endpoints | trustify-backend | TC-9006: trustify-backend |
| Task 3 | Add integration tests for remediation endpoints | trustify-backend | TC-9006: trustify-backend |
| Task 4 | Add remediation API client, models, and React Query hooks | trustify-ui | TC-9006: trustify-ui |
| Task 5 | Create remediation dashboard page with summary cards and progress chart | trustify-ui | TC-9006: trustify-ui |
| Task 6 | Add filterable vulnerability table to remediation dashboard | trustify-ui | TC-9006: trustify-ui |
| Task 7 | Add frontend tests for remediation dashboard | trustify-ui | TC-9006: trustify-ui |
| Task 8 | Document remediation dashboard and aggregation endpoints | trustify-backend | TC-9006: trustify-backend |

---

## Task additional_fields (applied to all created tasks)

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

- **priority**: propagated from Feature TC-9006 (Major)
- **fixVersions**: propagated from Feature TC-9006 (RHTPA 1.5.0); `fixVersion scope` is "both" per Jira Field Defaults, so propagation is active

---

## Inherited Field Values

- **Priority:** Major (inherited from Feature TC-9006, propagated to all Epics and Tasks)
- **Fix Versions:** RHTPA 1.5.0 (inherited from Feature TC-9006, propagated to all Epics and Tasks per fixVersion scope "both")

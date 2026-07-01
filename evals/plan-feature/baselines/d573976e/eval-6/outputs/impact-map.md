# Repository Impact Map — TC-9006

## Feature: Add vulnerability remediation tracking dashboard

---

### trustify-backend

**Changes:**

- Add `GET /api/v2/remediation/summary` endpoint that returns aggregated vulnerability counts grouped by severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved)
- Add `GET /api/v2/remediation/by-product` endpoint that returns per-product remediation breakdown with total, open, and resolved counts
- Add remediation service module with aggregation logic computed from existing vulnerability and SBOM relationship data (no new database tables)
- Add remediation model structs (`RemediationSummary`, `ProductRemediation`) for API response types
- Add integration tests for the new remediation endpoints

### trustify-ui

**Changes:**

- Add API client functions for the remediation endpoints (`fetchRemediationSummary`, `fetchRemediationByProduct`)
- Add TypeScript interfaces for remediation API response types
- Add React Query hooks for remediation data fetching (`useRemediationSummary`, `useRemediationByProduct`)
- Add `/remediation` dashboard page with summary cards (Open, In Progress, Resolved counts), progress chart (30-day trend), and filterable vulnerability table
- Add route definition for `/remediation` path
- Add remediation page components (SummaryCards, ProgressChart, VulnerabilityTable with severity/product/status filters)
- Add unit tests for the remediation dashboard page and components
- Add MSW mock handlers and fixture data for remediation endpoints

---

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** This feature exhibits **tightly coupled feature components** (atomicity indicator #4). The frontend dashboard page at `/remediation` requires the backend `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product` endpoints to function. Merging the frontend without the backend would result in a broken page with no data sources. Merging the backend alone would be harmless but incomplete. Both sides must land together for the feature to be usable.

The `workflow:feature-branch` label will be applied to the feature issue TC-9006.

---

## Epic Grouping

**Strategy:** `by-repository` (from CLAUDE.md Hierarchy Configuration)

| Epic | Repository | Tasks |
|---|---|---|
| TC-9006: trustify-backend | trustify-backend | Tasks 2, 3 |
| TC-9006: trustify-ui | trustify-ui | Tasks 4, 5, 6 |

Bookend tasks (Task 1: create-branch, Task 7: merge-branch) are not assigned to Epics.

---

## Field Inheritance

- **Priority:** Major (inherited from TC-9006, propagated to all Epics and Tasks)
- **Fix Versions:** RHTPA 1.5.0 (inherited from TC-9006, propagated to all Epics and Tasks — fixVersion scope defaults to "both")

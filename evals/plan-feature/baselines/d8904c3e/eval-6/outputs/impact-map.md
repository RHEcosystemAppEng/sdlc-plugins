# Repository Impact Map -- TC-9006: Add vulnerability remediation tracking dashboard

## trustify-backend

changes:
  - Add remediation model types (RemediationSummary, ProductRemediation structs) in a new remediation module under modules/fundamental/src/remediation/
  - Add RemediationService with aggregation queries for summary-by-severity-and-status and breakdown-by-product, computing from existing vulnerability and SBOM relationship data (no new database tables)
  - Add GET /api/v2/remediation/summary endpoint returning aggregated counts by severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved)
  - Add GET /api/v2/remediation/by-product endpoint returning per-product remediation breakdown (total, open, resolved counts per product)
  - Register remediation routes in server/src/main.rs
  - Add integration tests for both remediation endpoints in tests/api/

## trustify-ui

changes:
  - Add TypeScript interfaces for remediation API response types in src/api/models.ts
  - Add API client functions (fetchRemediationSummary, fetchRemediationByProduct) in src/api/rest.ts
  - Add React Query hooks (useRemediationSummary, useRemediationByProduct) in src/hooks/
  - Add RemediationDashboardPage with summary cards (Open, In Progress, Resolved counts) and progress chart (30-day trend) in src/pages/RemediationDashboardPage/
  - Add filterable vulnerability table component with severity, product, and status filters in src/pages/RemediationDashboardPage/components/
  - Register /remediation route in src/routes.tsx and add navigation entry in src/App.tsx
  - Add unit tests (Vitest + RTL), MSW mock handlers, and Playwright E2E tests for the remediation dashboard

## Excluded requirements

- **CSV export of remediation report**: marked as non-MVP in the feature requirements. Cannot be planned without further specification on export format, file naming, and download UX. Will be addressed in a follow-up feature iteration.

## Workflow Mode

**Selected mode:** `feature-branch`

**Rationale:** Atomicity indicator 4 (tightly coupled feature components) is present -- the frontend remediation dashboard page at `/remediation` requires the backend `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product` endpoints that do not yet exist. Merging the frontend without the backend would result in a non-functional dashboard page. All tasks are interdependent across repositories: backend tasks 2-4 produce the API that frontend tasks 5-9 consume.

The `workflow:feature-branch` label will be applied to the TC-9006 feature issue.

## Epic Hierarchy

Grouping strategy: **by-repository** (from CLAUDE.md Hierarchy Configuration)

| Epic | Summary | Issue Type | Parent |
|------|---------|------------|--------|
| Epic 1 | TC-9006: trustify-backend | Epic (level 1) | TC-9006 |
| Epic 2 | TC-9006: trustify-ui | Epic (level 1) | TC-9006 |

Feature "Incorporates" links go from TC-9006 to each Epic (not to individual Tasks).

## Task-to-Epic Assignment

| Task | Summary | Epic |
|------|---------|------|
| Task 1 | Create feature branch TC-9006 from main | TC-9006: trustify-ui |
| Task 2 | Add remediation model types and aggregation service | TC-9006: trustify-backend |
| Task 3 | Add remediation API endpoints and register routes | TC-9006: trustify-backend |
| Task 4 | Add integration tests for remediation endpoints | TC-9006: trustify-backend |
| Task 5 | Add API client functions and TypeScript models for remediation endpoints | TC-9006: trustify-ui |
| Task 6 | Add React Query hooks for remediation data fetching | TC-9006: trustify-ui |
| Task 7 | Add remediation dashboard page with summary cards, progress chart, and route registration | TC-9006: trustify-ui |
| Task 8 | Add filterable vulnerability table to remediation dashboard | TC-9006: trustify-ui |
| Task 9 | Add unit and E2E tests for remediation dashboard | TC-9006: trustify-ui |
| Task 10 | Document remediation dashboard and API endpoints | TC-9006: trustify-ui |
| Task 11 | Merge feature branch TC-9006 to main | TC-9006: trustify-ui |

## Inherited Field Values

- **Priority**: Major (inherited from TC-9006, propagated to all Epics and Tasks)
- **fixVersions**: RHTPA 1.5.0 (inherited from TC-9006, propagated to all Epics and Tasks; no `fixVersion scope` configured in Jira Field Defaults, defaulting to "both")

## Epic Creation Details

### Epic 1: TC-9006: trustify-backend

```
jira.create_issue(
  projectKey="TC",
  issueTypeName="Epic",
  summary="TC-9006: trustify-backend",
  description="Backend implementation for the vulnerability remediation tracking dashboard. Includes remediation model types, aggregation service computing from existing vulnerability and SBOM relationship data, REST API endpoints for summary and by-product breakdowns, and integration tests.",
  parent="TC-9006",
  additional_fields={
    "labels": ["ai-generated-jira"],
    "priority": {"name": "Major"},
    "fixVersions": [{"name": "RHTPA 1.5.0"}]
  }
)
```

### Epic 2: TC-9006: trustify-ui

```
jira.create_issue(
  projectKey="TC",
  issueTypeName="Epic",
  summary="TC-9006: trustify-ui",
  description="Frontend implementation for the vulnerability remediation tracking dashboard. Includes API client functions, React Query hooks, dashboard page with summary cards and progress chart, filterable vulnerability table, route registration, tests, and documentation.",
  parent="TC-9006",
  additional_fields={
    "labels": ["ai-generated-jira"],
    "priority": {"name": "Major"},
    "fixVersions": [{"name": "RHTPA 1.5.0"}]
  }
)
```

## Issue Links

### Feature to Epics (Incorporates)

- TC-9006 **Incorporates** Epic 1 (TC-9006: trustify-backend)
- TC-9006 **Incorporates** Epic 2 (TC-9006: trustify-ui)

### Task Dependencies (Depend)

- Task 3 **depends on** Task 2
- Task 4 **depends on** Task 3
- Task 5 **depends on** Task 3
- Task 6 **depends on** Task 5
- Task 7 **depends on** Task 6
- Task 8 **depends on** Task 7
- Task 9 **depends on** Task 7, Task 8
- Task 10 **depends on** Task 4, Task 9
- Task 11 **depends on** Tasks 2-10
- All non-documentation intermediate tasks (2-9) also depend on Task 1 (create-branch bookend)

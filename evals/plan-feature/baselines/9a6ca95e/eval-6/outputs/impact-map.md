# Repository Impact Map -- TC-9006: Vulnerability Remediation Tracking Dashboard

## Epic Creation Plan

A level-1 issue type (Epic) is available. Grouping strategy: **by-repository** (one Epic per repository).

| Epic | Summary | Parent | Issue Type |
|---|---|---|---|
| Epic 1 | TC-9006: trustify-backend | TC-9006 | Epic (level-1) |
| Epic 2 | TC-9006: trustify-ui | TC-9006 | Epic (level-1) |

### Issue Links

- **Incorporates**: TC-9006 incorporates Epic 1 (TC-9006: trustify-backend)
- **Incorporates**: TC-9006 incorporates Epic 2 (TC-9006: trustify-ui)

Note: Incorporates links go from Feature to Epics, not from Feature to Tasks. Tasks inherit hierarchy through their Epic parent.

## Repository Changes

### trustify-backend

Changes:
- Add remediation model types (RemediationSummary, ProductRemediation structs) in a new remediation sub-module under modules/fundamental/src/
- Add remediation aggregation service that computes counts from existing advisory, SBOM, and join table entities
- Add `GET /api/v2/remediation/summary` endpoint returning aggregated counts by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved)
- Add `GET /api/v2/remediation/by-product` endpoint returning per-product remediation breakdown with total, open, and resolved counts
- Mount remediation routes in server/src/main.rs
- Add integration tests for both remediation endpoints in tests/api/

### trustify-ui

Changes:
- Add TypeScript interfaces for remediation API response types in src/api/models.ts
- Add API client functions (fetchRemediationSummary, fetchRemediationByProduct) in src/api/rest.ts
- Add React Query hooks (useRemediationSummary, useRemediationByProduct) in src/hooks/
- Create RemediationDashboardPage with summary cards (Open, In Progress, Resolved counts) and a progress chart showing remediation trend
- Add filterable vulnerability table component with severity, product, and status filters
- Register /remediation route in src/routes.tsx and add navigation entry in src/App.tsx

## Task-to-Epic Assignment

| Task | Repository | Parent Epic |
|---|---|---|
| Task 1: Add remediation model types and aggregation service | trustify-backend | Epic 1 (TC-9006: trustify-backend) |
| Task 2: Add remediation REST endpoints | trustify-backend | Epic 1 (TC-9006: trustify-backend) |
| Task 3: Add integration tests for remediation endpoints | trustify-backend | Epic 1 (TC-9006: trustify-backend) |
| Task 4: Add remediation API client functions and React Query hooks | trustify-ui | Epic 2 (TC-9006: trustify-ui) |
| Task 5: Create remediation dashboard page with summary cards and progress chart | trustify-ui | Epic 2 (TC-9006: trustify-ui) |
| Task 6: Add filterable vulnerability table to remediation dashboard | trustify-ui | Epic 2 (TC-9006: trustify-ui) |
| Task 7: Add route and navigation for remediation dashboard | trustify-ui | Epic 2 (TC-9006: trustify-ui) |
| Task 8: Document remediation dashboard and API endpoints | trustify-ui | Epic 2 (TC-9006: trustify-ui) |

## Workflow Mode

**Mode:** direct-to-main

**Rationale:** No atomicity indicators identified. The backend endpoints can be merged to main independently (they add new endpoints without breaking existing ones). The frontend can be merged after the backend is available. No coordinated schema migrations, breaking API changes, or cross-cutting refactors are required.

## Inherited Field Propagation

- **Priority**: Major -- propagated to all Epics and Tasks
- **fixVersions**: RHTPA 1.5.0 -- propagated to all Epics and Tasks (fixVersion scope defaults to "both")

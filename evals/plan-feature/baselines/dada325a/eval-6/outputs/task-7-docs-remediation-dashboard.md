<!-- Jira creation metadata (simulated; not part of the description body) -->
<!-- Summary: Document the remediation dashboard and aggregation endpoints | Simulated key: TC-9109 | Issue type: Task | Parent Epic: TC-9102 (TC-9006: trustify-ui) | Labels: ai-generated-jira | Priority: Major | fixVersions: RHTPA 1.5.0 -->

## Repository
trustify-ui

## Target Branch
main

## Description
Document the new vulnerability remediation tracking dashboard delivered by TC-9006.

**What changed:** a new `/remediation` dashboard page shows portfolio-wide remediation progress with summary cards (Open / In Progress / Resolved), a 30-day progress chart, and a filterable table of outstanding vulnerabilities (filter by severity, product, status). It is backed by three new aggregation endpoints in trustify-backend: `GET /api/v2/remediation/summary`, `GET /api/v2/remediation/by-product`, and `GET /api/v2/remediation/vulnerabilities`.

**Doc impact type:** New Content.

**Details from Documentation Considerations:** document the remediation dashboard and the aggregation endpoints. User purpose: security teams need a guide for using the dashboard (viewing the summary, filtering by product/severity/status, drilling down to individual vulnerabilities); API consumers need an endpoint reference (paths, query parameters, response shapes). Note for readers that remediation status depends on advisory correlation being up to date.

Feature reference: TC-9006.

## Acceptance Criteria
- [ ] A user guide for the remediation dashboard exists covering UC-1 (view remediation summary) and UC-2 (filter by product)
- [ ] The guide explains summary cards, the 30-day progress chart, and the severity/product/status filters
- [ ] An endpoint reference documents `GET /api/v2/remediation/summary`, `GET /api/v2/remediation/by-product`, and `GET /api/v2/remediation/vulnerabilities` with parameters and response shapes
- [ ] The documentation notes that remediation status depends on up-to-date advisory correlation

## Test Requirements
- [ ] Verify every documented endpoint path, parameter, and response field matches the implemented backend behavior
- [ ] Verify the dashboard walkthrough matches the implemented UI (labels, filters, default views)
- [ ] Verify documentation links resolve

## Dependencies
- Depends on: Task 1 — Add remediation module with summary aggregation endpoint
- Depends on: Task 2 — Add per-product remediation breakdown endpoint
- Depends on: Task 3 — Add filterable remediation vulnerability list endpoint
- Depends on: Task 4 — Add remediation API models, client functions, and React Query hooks
- Depends on: Task 5 — Add remediation dashboard page with summary cards and progress chart
- Depends on: Task 6 — Add filterable vulnerability table to remediation dashboard

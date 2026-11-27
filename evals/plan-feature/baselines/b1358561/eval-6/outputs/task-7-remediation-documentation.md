**Summary:** Document the remediation tracking dashboard and remediation aggregation endpoints
**Parent Epic:** TC-9101 (TC-9006: trustify-backend)
**Issue type:** Task | **Labels:** ai-generated-jira | **Priority:** Major | **fixVersions:** RHTPA 1.5.0

## Repository
trustify-backend

## Target Branch
main

## Description
Feature TC-9006 adds a vulnerability remediation tracking dashboard (`/remediation` in trustify-ui) backed by new aggregation endpoints in trustify-backend (`GET /api/v2/remediation/summary`, `GET /api/v2/remediation/by-product`, `GET /api/v2/remediation/vulnerabilities`, `GET /api/v2/remediation/trend`).

**Doc impact type:** New Content — document the remediation dashboard and aggregation endpoints.

**Details from Documentation Considerations:**
- Security teams need a user guide for the dashboard: summary cards (Open / In Progress / Resolved), the 30-day remediation trend chart, and the filterable vulnerability table (filter by severity, product, status; sort by severity).
- API consumers need an endpoint reference for the remediation endpoints: paths, query parameters (filters, pagination, `days`), and response shapes.
- Note the customer consideration that remediation status depends on advisory correlation being up to date, and that the product breakdown is paginated for large portfolios (>50 products).

Reference: Feature TC-9006.

## Acceptance Criteria
- [ ] A dashboard user guide describes navigating to `/remediation`, reading summary cards and the trend chart, and filtering/sorting the vulnerability table
- [ ] An API reference documents all four `/api/v2/remediation/*` endpoints with parameters and response shapes matching the implemented behavior
- [ ] The documentation states that remediation status depends on up-to-date advisory correlation
- [ ] The documentation covers pagination of the per-product breakdown

## Test Requirements
- [ ] Verify each documented endpoint path, parameter and response field against the implemented handlers (Tasks 2 and 3)
- [ ] Verify the user guide steps against the running dashboard (Tasks 5 and 6), including filter and sort behavior
- [ ] Verify documentation is complete for every item listed in the Feature's Documentation Considerations

## Dependencies
- Depends on: Task 1 — Add remediation domain module with summary and per-product aggregation service
- Depends on: Task 2 — Add GET /api/v2/remediation/summary and /api/v2/remediation/by-product endpoints
- Depends on: Task 3 — Add filterable remediation vulnerability list and 30-day trend endpoints
- Depends on: Task 4 — Add remediation API types, REST client functions, React Query hooks and MSW mocks
- Depends on: Task 5 — Add /remediation dashboard page with summary cards and remediation trend chart
- Depends on: Task 6 — Add filterable outstanding-vulnerability table to the remediation dashboard

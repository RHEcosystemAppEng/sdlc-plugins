## Repository
trustify-backend

## Target Branch
main

## Description
Document the vulnerability remediation tracking dashboard and its aggregation endpoints delivered by Feature TC-9006.

**What changed:** TC-9006 adds three backend endpoints — `GET /api/v2/remediation/summary` (counts by severity × status), `GET /api/v2/remediation/by-product` (paginated per-product breakdown), and `GET /api/v2/remediation/vulnerabilities` (filterable list of outstanding vulnerabilities) — and a new UI dashboard at `/remediation` with summary cards, a progress chart, and a filterable table (severity, product, status).

**Doc impact type:** New Content — document the remediation dashboard and aggregation endpoints.

**Details from Documentation Considerations:** Security teams need a guide for using the dashboard (navigating to `/remediation`, reading the summary cards and chart, filtering by product/severity/status as in UC-1 and UC-2); API consumers need an endpoint reference (paths, query parameters, response shapes, pagination). Note the customer consideration that remediation status depends on advisory correlation being up to date.

Reference: Feature TC-9006.

## Acceptance Criteria
- [ ] Endpoint reference covers all three remediation endpoints with query parameters, response fields, and pagination behaviour as implemented
- [ ] User guide describes the `/remediation` dashboard: summary cards, progress chart, and filtering the vulnerability table by severity, product, and status
- [ ] Documentation states that remediation status depends on up-to-date advisory correlation
- [ ] Documentation matches the behaviour of the merged implementation (field names, status labels, filters)

## Test Requirements
- [ ] Verify every documented endpoint path, parameter, and response field against the implemented handlers and models in `modules/fundamental/src/remediation/`
- [ ] Walk through UC-1 and UC-2 in a running environment following the guide and confirm each step is accurate
- [ ] Peer review confirms the documentation is complete and consistent with the feature scope

## Dependencies
- Depends on: Task 1 — Add remediation module and summary endpoint
- Depends on: Task 2 — Add remediation by-product endpoint
- Depends on: Task 3 — Add remediation vulnerability list endpoint
- Depends on: Task 4 — Add remediation API client types and React Query hooks
- Depends on: Task 5 — Create remediation dashboard page with summary cards and progress chart
- Depends on: Task 6 — Add filterable remediation vulnerability table

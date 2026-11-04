## Repository
trustify-backend

## Target Branch
main

## Description
Documentation task for TC-9006 (Add vulnerability remediation tracking dashboard).

**Doc impact type:** New Content

**What changed:** The backend adds remediation aggregation endpoints —
`GET /api/v2/remediation/summary` (counts by severity × status),
`GET /api/v2/remediation/by-product` (paginated per-product breakdown), and
`GET /api/v2/remediation/vulnerabilities` (filterable list) — and the UI adds a
`/remediation` dashboard with summary cards, a progress chart, and a filterable
vulnerability table (filter by severity, product, status).

**Details from Documentation Considerations:** Document the remediation dashboard
and the aggregation endpoints. User purpose: security teams need a guide for using
the dashboard; API consumers need an endpoint reference. Note the customer
consideration that remediation status depends on advisory correlation being up to
date, and that the product breakdown is paginated for large portfolios.

Reference: Feature TC-9006.

Parent Epic: TC-9006: trustify-backend

## Acceptance Criteria
- [ ] API reference documents all three remediation endpoints with paths, query parameters, and response shapes matching the implementation
- [ ] User guide explains how to reach `/remediation`, read the summary cards and chart, and filter/sort the vulnerability table (UC-1, UC-2)
- [ ] Documentation states that remediation status depends on up-to-date advisory correlation
- [ ] Documentation does not describe deferred functionality (CSV export, 30-day trend) as available

## Test Requirements
- [ ] Verify every documented endpoint, parameter, and response field against the merged implementation
- [ ] Walk through the user guide steps against a running instance and confirm they match the UI
- [ ] Review for completeness against the Documentation Considerations scope of TC-9006

## Dependencies
- Depends on: Task 1 — Add remediation module and GET /api/v2/remediation/summary endpoint
- Depends on: Task 2 — Add GET /api/v2/remediation/by-product endpoint
- Depends on: Task 3 — Add GET /api/v2/remediation/vulnerabilities filterable list endpoint
- Depends on: Task 5 — Create remediation dashboard page with summary cards and progress chart
- Depends on: Task 6 — Add filterable vulnerability table to remediation dashboard

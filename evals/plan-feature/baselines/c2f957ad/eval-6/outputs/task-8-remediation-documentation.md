## Repository
trustify-ui

## Target Branch
main

## Description
Document the vulnerability remediation tracking dashboard delivered by TC-9006.

- **What changed:** a new `/remediation` dashboard page with summary cards (Open / In Progress / Resolved), a 30-day remediation trend chart, and a filterable (severity, product, status) table of outstanding vulnerabilities, backed by new aggregation endpoints `GET /api/v2/remediation/summary`, `GET /api/v2/remediation/by-product`, `GET /api/v2/remediation/vulnerabilities`, and `GET /api/v2/remediation/trend`.
- **Doc impact type:** New Content.
- **Details from Documentation Considerations:** document the remediation dashboard and the aggregation endpoints. User purpose: security teams need a guide for using the dashboard; API consumers need an endpoint reference.
- **Feature reference:** TC-9006.

Note: per-endpoint README entries in trustify-backend are added by Tasks 2–4 (Documentation Updates). This task produces the user-facing dashboard guide and a consolidated API reference for consumers.

## Acceptance Criteria
- [ ] A user guide explains how to reach `/remediation`, read the summary cards and trend chart, and filter/sort the vulnerability table (UC-1 and UC-2)
- [ ] An API reference covers all four remediation endpoints with parameters and response shapes matching the implemented behavior
- [ ] Documentation notes that remediation status depends on advisory correlation being up to date
- [ ] Documentation notes pagination of the product breakdown for large portfolios

## Test Requirements
- [ ] Verify every documented endpoint, parameter, and response field against the implemented backend
- [ ] Walk through UC-1 and UC-2 in a running environment following the guide and confirm the steps are accurate and complete
- [ ] Confirm UI labels in the guide match the rendered dashboard

## Dependencies
- Depends on: Task 2 — Remediation summary and by-product endpoints
- Depends on: Task 3 — Remediation vulnerability list endpoint
- Depends on: Task 4 — Remediation trend endpoint
- Depends on: Task 6 — Remediation dashboard page
- Depends on: Task 7 — Remediation vulnerability table

## Repository
trustify-backend

## Target Branch
main

## Description
Document the remediation dashboard feature and the new aggregation REST endpoints. The feature's Documentation Considerations section specifies "New Content" impact: security teams need a guide for using the dashboard, and API consumers need an endpoint reference for the two new remediation endpoints.

Doc impact type: New Content
Details: Security teams need a guide for using the dashboard; API consumers need endpoint reference for `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`.

Reference: Feature TC-9006 — Add vulnerability remediation tracking dashboard.

## Acceptance Criteria
- [ ] API endpoint reference documents `GET /api/v2/remediation/summary` with request parameters, response shape, and example response
- [ ] API endpoint reference documents `GET /api/v2/remediation/by-product` with request parameters, response shape, and example response
- [ ] Dashboard usage guide explains navigation to `/remediation`, summary cards, progress chart, and filterable table
- [ ] Documentation covers filtering by severity, product, and status
- [ ] Documentation accurately reflects the implemented feature behavior

## Test Requirements
- [ ] Verify all endpoint paths and response shapes match the actual implementation
- [ ] Verify dashboard navigation instructions are accurate
- [ ] Verify filter descriptions match available filter options

## Dependencies
- Depends on: Task 1 — Create remediation model and service layer
- Depends on: Task 2 — Add remediation REST endpoints
- Depends on: Task 3 — Add integration tests for remediation endpoints
- Depends on: Task 4 — Add remediation API client, models, and React Query hooks
- Depends on: Task 5 — Create remediation dashboard page with summary cards and progress chart
- Depends on: Task 6 — Add filterable vulnerability table to remediation dashboard
- Depends on: Task 7 — Add frontend tests for remediation dashboard

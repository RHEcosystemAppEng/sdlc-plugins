## Repository
trustify-ui

## Target Branch
main

## Description
Document the new remediation tracking dashboard and aggregation API endpoints. The feature description's Documentation Considerations section specifies doc impact type "New Content" with the following scope: security teams need a guide for using the dashboard, and API consumers need an endpoint reference for the remediation aggregation endpoints (`GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`).

This documentation covers:
- User guide for the remediation dashboard page at `/remediation`
- API reference for the two new remediation endpoints
- Description of summary cards, progress chart, and filterable vulnerability table functionality

Reference: Feature TC-9006 — Add vulnerability remediation tracking dashboard

## Acceptance Criteria
- [ ] Documentation accurately describes the remediation dashboard UI including summary cards, progress chart, and filterable vulnerability table
- [ ] API reference documents both `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product` with request/response shapes
- [ ] Documentation describes filtering capabilities (by severity, product, and status)
- [ ] Documentation is consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify documentation accurately reflects the implemented dashboard layout and functionality
- [ ] Verify API endpoint documentation matches the actual request/response contracts
- [ ] Verify all user-facing features (summary cards, chart, filters, table) are covered

## Dependencies
- Depends on: Task 1 — Create remediation module with summary endpoint
- Depends on: Task 2 — Add remediation by-product endpoint
- Depends on: Task 3 — Add integration tests for remediation endpoints
- Depends on: Task 4 — Add remediation API types, client functions, and React Query hooks
- Depends on: Task 5 — Create remediation dashboard page with summary cards and progress chart
- Depends on: Task 6 — Add filterable vulnerability table to remediation dashboard
- Depends on: Task 7 — Add tests for remediation dashboard

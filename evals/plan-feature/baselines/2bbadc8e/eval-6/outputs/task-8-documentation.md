## Repository
trustify-backend

## Target Branch
main

## Description
Add documentation for the vulnerability remediation tracking dashboard feature (TC-9006). The feature introduces two new backend API endpoints (GET /api/v2/remediation/summary and GET /api/v2/remediation/by-product) and a frontend dashboard page at /remediation. Documentation Considerations from the feature indicate New Content is needed: security teams need a guide for using the dashboard, and API consumers need endpoint reference documentation.

Doc impact type: New Content
Details: Security teams need a guide for using the dashboard; API consumers need endpoint reference.

## Acceptance Criteria
- [ ] API reference documentation covers GET /api/v2/remediation/summary with request parameters, response shape, and example response
- [ ] API reference documentation covers GET /api/v2/remediation/by-product with pagination parameters, response shape, and example response
- [ ] User guide documents the remediation dashboard page at /remediation, including summary cards, progress chart, and filterable table
- [ ] User guide covers filtering by severity, product, and status
- [ ] Documentation accurately reflects the implemented feature behavior

## Test Requirements
- [ ] Verify API documentation examples match actual endpoint responses
- [ ] Verify user guide screenshots or descriptions match the implemented dashboard UI
- [ ] Verify all documented filter options are accurate and complete

## Dependencies
- Depends on: Task 1 — Add remediation model and aggregation service
- Depends on: Task 2 — Add remediation API endpoints
- Depends on: Task 3 — Add remediation endpoint integration tests
- Depends on: Task 4 — Add remediation API client and React Query hooks
- Depends on: Task 5 — Add remediation dashboard page with summary cards and progress chart
- Depends on: Task 6 — Add filterable vulnerability table to remediation dashboard
- Depends on: Task 7 — Add remediation dashboard tests

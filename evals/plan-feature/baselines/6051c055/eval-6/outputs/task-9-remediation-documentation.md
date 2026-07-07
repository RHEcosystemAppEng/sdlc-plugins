## Repository
trustify-backend

## Target Branch
main

## Description
Document the new vulnerability remediation tracking dashboard and aggregation API endpoints (TC-9006). The Feature's Documentation Considerations indicate "New Content" is needed:

- **Doc impact type**: New Content
- **User purpose**: Security teams need a guide for using the dashboard; API consumers need endpoint reference
- **Scope**: Document the remediation dashboard usage and the two new aggregation endpoints (GET /api/v2/remediation/summary, GET /api/v2/remediation/by-product)

This documentation task covers:
1. API endpoint reference for the two new remediation aggregation endpoints, including request parameters, response shapes, and example responses
2. User guide for the remediation dashboard page, including summary cards, progress chart, and filterable vulnerability table
3. Description of supported filters (severity, product, status) and how to use them for remediation tracking

## Acceptance Criteria
- [ ] API endpoint documentation covers GET /api/v2/remediation/summary with request/response details and example
- [ ] API endpoint documentation covers GET /api/v2/remediation/by-product with request/response details, pagination parameters, and example
- [ ] User guide describes the remediation dashboard layout (summary cards, progress chart, vulnerability table)
- [ ] User guide describes how to use filters for severity, product, and status
- [ ] Documentation accurately reflects the implemented feature behavior
- [ ] Documentation covers the scope identified in the Feature's Documentation Considerations section

## Test Requirements
- [ ] Verify API endpoint documentation matches the actual endpoint behavior (paths, parameters, response shapes)
- [ ] Verify user guide accurately describes the dashboard UI components and interactions
- [ ] Verify documentation is consistent with the implemented feature

## Dependencies
- Depends on: Task 1 — Create remediation domain models and aggregation service
- Depends on: Task 2 — Add remediation REST endpoints with route registration
- Depends on: Task 3 — Add integration tests for remediation endpoints
- Depends on: Task 4 — Add remediation API types, client functions, and React Query hooks
- Depends on: Task 5 — Create remediation dashboard page with summary cards and progress chart
- Depends on: Task 6 — Add filterable vulnerability table to remediation dashboard
- Depends on: Task 7 — Register remediation dashboard route and add navigation entry
- Depends on: Task 8 — Add unit and E2E tests for remediation dashboard

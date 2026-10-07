## Repository
trustify-backend

## Target Branch
main

## Description
Document the new vulnerability remediation tracking dashboard feature, including the backend aggregation API endpoints and the frontend dashboard user interface. This is new documentation content as identified in the Feature's Documentation Considerations section.

Doc impact type: New Content

Details: Security teams need a guide for using the remediation dashboard to track vulnerability remediation progress across their portfolio. API consumers need endpoint reference documentation for the `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product` endpoints, including request parameters, response shapes, and usage examples.

Reference: Feature TC-9006 — Add vulnerability remediation tracking dashboard

## Acceptance Criteria
- [ ] API reference documentation covers GET /api/v2/remediation/summary with request parameters and response examples
- [ ] API reference documentation covers GET /api/v2/remediation/by-product with pagination parameters and response examples
- [ ] User guide section explains how to navigate to and use the remediation dashboard
- [ ] Documentation covers filtering by severity, product, and status
- [ ] Documentation is accurate and consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify API endpoint documentation matches actual endpoint behavior
- [ ] Verify dashboard user guide accurately describes the UI components and interactions
- [ ] Verify documentation covers all use cases from the Feature description (UC-1: View remediation summary and UC-2: Filter by product)

## Dependencies
- Depends on: Task 1 — Add remediation module with model structs and aggregation service
- Depends on: Task 2 — Add remediation REST endpoints
- Depends on: Task 3 — Add integration tests for remediation endpoints
- Depends on: Task 4 — Add API client and React Query hooks for remediation endpoints
- Depends on: Task 5 — Add remediation dashboard page with summary cards and progress chart
- Depends on: Task 6 — Add filterable vulnerability table to remediation dashboard

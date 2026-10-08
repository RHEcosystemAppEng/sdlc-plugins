## Repository
trustify-backend

## Target Branch
main

## Description
Document the new remediation dashboard and aggregation API endpoints. The Feature's Documentation Considerations specify "New Content" — security teams need a guide for using the dashboard and API consumers need an endpoint reference. This task covers writing user-facing documentation for the remediation dashboard page and API reference documentation for the `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product` endpoints.

Doc impact type: New Content
Details: Security teams need a guide for using the dashboard; API consumers need endpoint reference.
Reference: Feature TC-9006

## Acceptance Criteria
- [ ] User guide documents how to navigate to the remediation dashboard at `/remediation`
- [ ] User guide documents summary cards, progress chart, and filterable table functionality
- [ ] User guide documents filtering by severity, product, and status
- [ ] API reference documents `GET /api/v2/remediation/summary` endpoint with request/response shapes
- [ ] API reference documents `GET /api/v2/remediation/by-product` endpoint with request/response shapes and pagination
- [ ] Documentation is accurate and consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify all endpoint paths and response shapes match the actual implementation
- [ ] Verify dashboard navigation path and UI descriptions match the implemented UI
- [ ] Verify filter options documented match the available filters in the implementation

## Dependencies
- Depends on: Task 1 — Add remediation module with summary aggregation endpoint
- Depends on: Task 2 — Add per-product remediation breakdown endpoint
- Depends on: Task 3 — Add API client functions and React Query hooks for remediation endpoints
- Depends on: Task 4 — Add remediation dashboard page with summary cards and progress chart
- Depends on: Task 5 — Add filterable vulnerability table to remediation dashboard

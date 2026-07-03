## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9006: trustify-ui

## Description
Document the new vulnerability remediation tracking dashboard and the backend aggregation API endpoints. The Feature description indicates New Content documentation is needed. Security teams need a guide for using the dashboard, and API consumers need endpoint reference documentation for the remediation summary and by-product endpoints.

Doc impact type: New Content
Reference: TC-9006 (Add vulnerability remediation tracking dashboard)

## Acceptance Criteria
- [ ] Documentation covers the remediation dashboard purpose and usage for security managers
- [ ] API endpoint reference documents GET /api/v2/remediation/summary with request/response shapes
- [ ] API endpoint reference documents GET /api/v2/remediation/by-product with request/response shapes
- [ ] Documentation describes available filters (severity, product, status) and how to use them
- [ ] Documentation is accurate and consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify documentation accurately reflects the dashboard's current functionality
- [ ] Verify API endpoint documentation matches the actual request/response contracts
- [ ] Verify filter documentation matches the available filter options in the UI

## Dependencies
- Depends on: Task 1 -- Add remediation model types and aggregation service
- Depends on: Task 2 -- Add remediation REST endpoints
- Depends on: Task 3 -- Add integration tests for remediation endpoints
- Depends on: Task 4 -- Add remediation API client functions and React Query hooks
- Depends on: Task 5 -- Create remediation dashboard page with summary cards and progress chart
- Depends on: Task 6 -- Add filterable vulnerability table to remediation dashboard
- Depends on: Task 7 -- Add route and navigation for remediation dashboard

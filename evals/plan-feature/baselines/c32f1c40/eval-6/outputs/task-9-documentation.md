## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Document the vulnerability remediation tracking dashboard and the backend aggregation endpoints. The feature introduces new user-facing functionality (remediation dashboard at `/remediation`) and new API endpoints (`GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`) that require documentation for security teams using the dashboard and API consumers needing endpoint reference.

Doc impact type: New Content. Security teams need a guide for using the dashboard; API consumers need endpoint reference.

Reference: Feature TC-9006.

## Acceptance Criteria
- [ ] Documentation covers the remediation dashboard page and its features (summary cards, progress chart, filterable table)
- [ ] Documentation covers the GET /api/v2/remediation/summary endpoint (path, method, response shape, query parameters)
- [ ] Documentation covers the GET /api/v2/remediation/by-product endpoint (path, method, response shape, pagination parameters)
- [ ] Documentation describes the filtering capabilities (by severity, product, status)
- [ ] Documentation is accurate and consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify documentation accurately describes the dashboard's summary cards, progress chart, and vulnerability table
- [ ] Verify API endpoint documentation matches the actual request/response shapes
- [ ] Verify all filter options are documented (severity, product, status)
- [ ] Verify documentation is complete and does not reference unimplemented features (e.g., CSV export)

## Dependencies
- Depends on: Task 2 -- Add remediation data models and aggregation service
- Depends on: Task 3 -- Add remediation summary and by-product REST endpoints
- Depends on: Task 4 -- Add remediation endpoint integration tests
- Depends on: Task 5 -- Add remediation API types, client functions, and React Query hooks
- Depends on: Task 6 -- Create remediation dashboard page with summary cards and progress chart
- Depends on: Task 7 -- Add filterable vulnerability table to remediation dashboard
- Depends on: Task 8 -- Add remediation dashboard unit and E2E tests

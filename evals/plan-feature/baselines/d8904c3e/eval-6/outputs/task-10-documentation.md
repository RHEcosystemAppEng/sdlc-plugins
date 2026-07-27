## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Document the new vulnerability remediation tracking dashboard and the backend aggregation API endpoints. The Feature's Documentation Considerations indicate "New Content" is needed. Security teams need a user guide for the dashboard, and API consumers need endpoint reference documentation. This task covers both the user-facing dashboard guide and the API reference.

Doc impact type: New Content
Details: Security teams need a guide for using the dashboard; API consumers need endpoint reference.

Reference: Feature TC-9006

## Acceptance Criteria
- [ ] Dashboard user guide documents navigation to /remediation, summary cards interpretation, progress chart usage, and filter interactions
- [ ] API reference documents GET /api/v2/remediation/summary endpoint with request parameters and response shape
- [ ] API reference documents GET /api/v2/remediation/by-product endpoint with pagination parameters and response shape
- [ ] Documentation accurately reflects the implemented feature behavior
- [ ] Documentation covers all scope identified in Feature Documentation Considerations (user guide + API reference)

## Test Requirements
- [ ] Verify documentation accurately describes the dashboard UI and its components
- [ ] Verify API endpoint documentation matches actual request/response shapes
- [ ] Verify documentation is complete and consistent with implemented feature behavior

## Dependencies
- Depends on: Task 4 -- Add integration tests for remediation endpoints
- Depends on: Task 9 -- Add unit and E2E tests for remediation dashboard

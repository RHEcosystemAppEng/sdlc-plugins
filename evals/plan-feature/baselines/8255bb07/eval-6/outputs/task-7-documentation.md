## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9007 (TC-9006: trustify-backend)

## Description
Document the new remediation dashboard and aggregation API endpoints introduced by feature TC-9006. The Feature's Documentation Considerations indicate "New Content" is needed: security teams need a guide for using the dashboard, and API consumers need an endpoint reference for the remediation aggregation APIs.

Documentation should cover:
- API endpoint reference for GET /api/v2/remediation/summary, GET /api/v2/remediation/by-product, and GET /api/v2/remediation/export/csv
- Request parameters, response shapes, and example responses for each endpoint
- Dashboard usage guide for security managers: navigating to /remediation, interpreting summary cards and progress chart, using filters to drill down by severity, product, and status
- Use case walkthroughs matching UC-1 (view remediation summary) and UC-2 (filter by product) from the Feature description

Doc impact type: New Content
Reference: Feature TC-9006

## Acceptance Criteria
- [ ] API endpoint reference documents all three remediation endpoints with request/response shapes
- [ ] Each endpoint includes at least one example request and response
- [ ] Dashboard usage guide covers navigating to /remediation and interpreting the summary view
- [ ] Filter usage is documented (severity, product, status filter interactions)
- [ ] Documentation accurately reflects the implemented feature behavior
- [ ] Documentation covers the scope identified in Feature TC-9006 Documentation Considerations

## Test Requirements
- [ ] Verify API endpoint documentation matches actual endpoint behavior (paths, parameters, response shapes)
- [ ] Verify dashboard usage guide screenshots or descriptions match the implemented UI
- [ ] Verify documentation is consistent with both backend API and frontend dashboard implementations

## Dependencies
- Depends on: Task 2 — Add remediation API endpoints with integration tests
- Depends on: Task 3 — Add CSV export endpoint for remediation report
- Depends on: Task 5 — Add remediation dashboard page with summary cards and progress chart
- Depends on: Task 6 — Add filterable vulnerability table to remediation dashboard

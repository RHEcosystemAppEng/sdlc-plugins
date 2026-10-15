## Repository
trustify-backend

## Target Branch
main

## Description
Document the vulnerability remediation tracking dashboard and its API endpoints (TC-9006). This task covers new documentation content as identified in the Feature's Documentation Considerations: security teams need a guide for using the dashboard, and API consumers need endpoint reference documentation for the new remediation aggregation endpoints.

**Doc impact type:** New Content

The documentation should cover:
- The remediation dashboard purpose and user workflow (navigating to /remediation, interpreting summary cards, using filters)
- API endpoint reference for GET /api/v2/remediation/summary (request parameters, response shape, example)
- API endpoint reference for GET /api/v2/remediation/by-product (request parameters, response shape, pagination, example)
- How remediation data is aggregated from existing vulnerability and SBOM data

## Acceptance Criteria
- [ ] Dashboard user guide documents how to navigate to and use the remediation dashboard
- [ ] API reference documents GET /api/v2/remediation/summary with request/response examples
- [ ] API reference documents GET /api/v2/remediation/by-product with pagination and request/response examples
- [ ] Documentation accurately reflects the implemented feature behavior
- [ ] Documentation covers the filter and sort capabilities described in the Feature requirements

## Test Requirements
- [ ] Verify documentation is accurate against the implemented API endpoints
- [ ] Verify dashboard user guide matches the actual UI layout and functionality
- [ ] Verify API examples return valid responses when tested against a running instance

## Dependencies
- Depends on: Task 1 — Add remediation model types and aggregation service
- Depends on: Task 2 — Add remediation REST endpoints
- Depends on: Task 3 — Add integration tests for remediation endpoints
- Depends on: Task 4 — Add remediation API types, client functions, and React Query hooks
- Depends on: Task 5 — Add remediation dashboard page with summary cards and progress chart
- Depends on: Task 6 — Add filterable vulnerability table to remediation dashboard

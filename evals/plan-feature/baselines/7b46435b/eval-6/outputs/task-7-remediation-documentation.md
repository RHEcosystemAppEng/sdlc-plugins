## Repository
trustify-ui

## Target Branch
main

## Description
Create documentation for the vulnerability remediation tracking dashboard feature. The Feature description's Documentation Considerations section indicates "New Content" is needed -- new documentation pages or sections covering both the user-facing dashboard and the backend API endpoints.

**Doc impact type**: New Content

**Documentation scope** (from Feature TC-9006 Documentation Considerations):
- Security teams need a guide for using the remediation dashboard (navigating summary cards, progress chart, and filterable vulnerability table)
- API consumers need endpoint reference for the aggregation endpoints (`GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`)

**Feature reference**: TC-9006 -- Add vulnerability remediation tracking dashboard

## Acceptance Criteria
- [ ] Documentation covers the remediation dashboard page location (`/remediation`) and its three sections: summary cards, progress chart, and filterable vulnerability table
- [ ] Documentation explains how to use filters (severity, product, status) to narrow vulnerability results
- [ ] Documentation covers the `GET /api/v2/remediation/summary` endpoint with request/response format and example
- [ ] Documentation covers the `GET /api/v2/remediation/by-product` endpoint with request/response format, pagination parameters, and example
- [ ] Documentation accurately reflects the implemented feature behavior
- [ ] Documentation is consistent with the existing documentation style and structure

## Test Requirements
- [ ] Verify documentation is accurate against the implemented API endpoint response shapes
- [ ] Verify all filter options (severity, product, status) are documented with correct value sets
- [ ] Verify API response examples match actual endpoint responses
- [ ] Verify dashboard navigation path and UI descriptions match the implemented UI

## Dependencies
- Depends on: Task 1 -- Add remediation module with summary aggregation endpoint
- Depends on: Task 2 -- Add remediation by-product breakdown endpoint
- Depends on: Task 3 -- Add remediation endpoint integration tests
- Depends on: Task 4 -- Add remediation API types, client functions, and React Query hooks
- Depends on: Task 5 -- Create remediation dashboard page with summary cards and progress chart
- Depends on: Task 6 -- Add filterable vulnerability table to remediation dashboard

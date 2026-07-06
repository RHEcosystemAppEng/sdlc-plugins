## Repository
trustify-ui

## Target Branch
main

## Description
Document the new vulnerability remediation tracking dashboard and the backend aggregation endpoints. The feature description indicates a doc impact type of "New Content" -- security teams need a guide for using the dashboard and API consumers need an endpoint reference for the remediation aggregation APIs.

Documentation should cover:
- Dashboard usage guide: navigating to `/remediation`, interpreting summary cards, reading the progress chart, using filters on the vulnerability table
- API endpoint reference: `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product` with request parameters and response shapes
- Feature context from TC-9006: vulnerability remediation tracking across ingested SBOMs

## Acceptance Criteria
- [ ] Dashboard usage guide documents how to navigate to and use the remediation dashboard
- [ ] Summary cards, progress chart, and filterable table are documented with their purpose and interactions
- [ ] API endpoint reference documents both endpoints with request parameters and response shapes
- [ ] Filter options (severity, product, status) are documented
- [ ] Documentation is consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify documentation accurately reflects the dashboard UI as implemented
- [ ] Verify API endpoint reference matches the actual endpoint behavior
- [ ] Verify all filter options documented match the implemented filters
- [ ] Verify response shape examples in documentation match actual API responses

## Dependencies
- Depends on: Task 1 -- Add remediation summary aggregation service and endpoint
- Depends on: Task 2 -- Add remediation by-product aggregation service and endpoint
- Depends on: Task 3 -- Add integration tests for remediation endpoints
- Depends on: Task 4 -- Add API client functions and React Query hooks for remediation endpoints
- Depends on: Task 5 -- Add remediation dashboard page with summary cards and progress chart
- Depends on: Task 6 -- Add filterable vulnerability table to remediation dashboard

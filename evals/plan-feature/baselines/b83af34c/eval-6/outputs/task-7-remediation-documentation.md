## Repository
trustify-backend

## Parent Epic
TC-9007 (TC-9006: trustify-backend)

## Priority
Major (inherited from Feature TC-9006)

## Fix Versions
RHTPA 1.5.0 (inherited from Feature TC-9006)

## Target Branch
main

## Description
Create documentation for the new remediation tracking dashboard and aggregation API endpoints. This covers the REST API reference for `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product` (request parameters, response schemas, example responses), and a user guide for security teams describing how to use the dashboard page to monitor remediation progress, apply filters, and interpret the summary cards and progress chart.

Documentation scope is "New Content" as specified in the feature's Documentation Considerations section.

## Acceptance Criteria
- [ ] API reference documents GET /api/v2/remediation/summary with request parameters and response schema
- [ ] API reference documents GET /api/v2/remediation/by-product with pagination parameters and response schema
- [ ] User guide describes navigating to the remediation dashboard at /remediation
- [ ] User guide explains summary cards, progress chart, and filterable vulnerability table
- [ ] User guide describes filtering by severity, product, and status
- [ ] Documentation follows existing project documentation style and format

## Test Requirements
- [ ] Review documentation for accuracy against implemented API endpoints
- [ ] Verify all documented request/response examples match actual endpoint behavior
- [ ] Verify dashboard usage instructions match the implemented UI

## Dependencies
- Depends on: Task 3 — remediation-integration-tests (backend implementation complete)
- Depends on: Task 6 — vulnerability-table (frontend implementation complete)

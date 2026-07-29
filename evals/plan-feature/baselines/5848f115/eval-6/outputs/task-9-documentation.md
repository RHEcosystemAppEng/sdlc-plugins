# Task 9 — Documentation: remediation dashboard and aggregation endpoints

## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Document the new vulnerability remediation tracking dashboard and the two aggregation API endpoints (`GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`). The Feature description's Documentation Considerations section indicates "New Content" doc impact: security teams need a guide for using the dashboard, and API consumers need endpoint reference documentation.

This task covers:
- New Content: document the remediation dashboard user guide (how to navigate, interpret summary cards, use filters)
- New Content: document the aggregation REST API endpoints (request/response shapes, query parameters, example responses)

The documentation should accurately reflect the feature's behavior as implemented in Tasks 2-8.

## Acceptance Criteria
- [ ] Dashboard user guide documents navigation to `/remediation`, summary cards interpretation, progress chart, and filter usage
- [ ] API endpoint reference documents `GET /api/v2/remediation/summary` with request/response shape and example response
- [ ] API endpoint reference documents `GET /api/v2/remediation/by-product` with pagination parameters and example response
- [ ] Documentation is consistent with the implemented feature behavior from TC-9006
- [ ] Documentation covers the scope identified in the Feature's Documentation Considerations (New Content for dashboard guide and endpoint reference)

## Test Requirements
- [ ] Verify documentation accurately reflects the implemented API endpoint paths and response shapes
- [ ] Verify dashboard guide covers all three dashboard sections (summary cards, progress chart, filterable table)
- [ ] Verify API examples are valid JSON matching the TypeScript interfaces and Rust model structs

## Dependencies
- Depends on: Task 5 — Add remediation endpoint integration tests
- Depends on: Task 8 — Add MSW mocks, fixtures, and E2E test for remediation dashboard

## Parent Epic
TC-9006: trustify-backend

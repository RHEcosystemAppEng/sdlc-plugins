## Repository
trustify-backend

## Target Branch
main

## Description
Document the new remediation dashboard feature and its backend aggregation endpoints. The Feature's Documentation Considerations specify "New Content" with doc impact: security teams need a guide for using the dashboard, and API consumers need endpoint reference documentation. This task covers API endpoint reference for `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`, including request/response shapes, query parameters, and example responses.

Doc impact type: New Content
Details: Security teams need a guide for using the dashboard; API consumers need endpoint reference.
Feature reference: TC-9006

## Acceptance Criteria
- [ ] API endpoint reference documents `GET /api/v2/remediation/summary` with request/response shape and example
- [ ] API endpoint reference documents `GET /api/v2/remediation/by-product` with request/response shape and example
- [ ] Documentation describes the remediation dashboard purpose and key features (summary cards, progress chart, filterable table)
- [ ] Documentation covers filtering capabilities (by severity, product, status)
- [ ] Documentation is accurate and consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify API endpoint documentation matches the actual endpoint behavior
- [ ] Verify example responses are valid JSON matching the actual response schema
- [ ] Verify all documented query parameters are correct and functional

## Dependencies
- Depends on: Task 1 — Add remediation model and aggregation service
- Depends on: Task 2 — Add remediation summary and by-product API endpoints
- Depends on: Task 3 — Add integration tests for remediation endpoints
- Depends on: Task 4 — Add remediation API types, client functions, and hooks
- Depends on: Task 5 — Create Remediation Dashboard page with summary cards and progress chart
- Depends on: Task 6 — Add filterable vulnerability table to remediation dashboard
- Depends on: Task 7 — Add tests for remediation dashboard

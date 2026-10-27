## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Document the new remediation tracking dashboard and aggregation endpoints. The Feature's Documentation Considerations indicate New Content is needed: security teams need a guide for using the dashboard, and API consumers need an endpoint reference for the new `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product` endpoints. This task covers both user-facing dashboard documentation and REST API reference documentation.

Reference: TC-9006 — Add vulnerability remediation tracking dashboard.

## Acceptance Criteria
- [ ] REST API reference documents both remediation endpoints with request/response schemas
- [ ] Dashboard usage guide explains navigation, summary cards, progress chart, and filters
- [ ] Documentation accurately reflects the implemented feature behavior
- [ ] Documentation covers the scope identified in the Feature's Documentation Considerations

## Test Requirements
- [ ] Documentation is accurate, complete, and consistent with the implemented feature behavior
- [ ] API endpoint documentation includes correct paths, methods, and response shapes
- [ ] Dashboard guide matches the actual UI layout and filter options

## Dependencies
- Depends on: Task 4 — Backend integration tests
- Depends on: Task 8 — Frontend tests

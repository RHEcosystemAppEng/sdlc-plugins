## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Document the new remediation tracking dashboard and its aggregation endpoints. The Feature's Documentation Considerations section indicates New Content is needed: a guide for security teams on using the dashboard and an API reference for the two new endpoints (`GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`).

Documentation scope from Feature TC-9006 Documentation Considerations:
- **Doc Impact**: New Content
- **User purpose**: Security teams need a guide for using the dashboard; API consumers need endpoint reference

## Acceptance Criteria
- [ ] Documentation covers the remediation dashboard page and its three main sections (summary cards, progress chart, filterable table)
- [ ] API reference documents GET /api/v2/remediation/summary with request/response shapes
- [ ] API reference documents GET /api/v2/remediation/by-product with request/response shapes
- [ ] Documentation describes filter options (severity, product, status)
- [ ] Documentation accurately reflects the implemented feature behavior

## Test Requirements
- [ ] Documentation is accurate and complete per the implemented feature
- [ ] API endpoint documentation matches actual response shapes
- [ ] No broken links or references to non-existent features

## Dependencies
- Depends on: Task 3 — Remediation endpoints
- Depends on: Task 4 — Backend integration tests
- Depends on: Task 7 — Remediation dashboard page

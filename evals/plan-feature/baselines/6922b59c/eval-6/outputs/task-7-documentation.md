## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Document the new vulnerability remediation tracking dashboard and its aggregation
API endpoints. The Feature's Documentation Considerations specify "New Content" impact:
security teams need a guide for using the dashboard, and API consumers need an endpoint
reference for `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`.

This task covers:
- **Doc Impact Type:** New Content
- **User purpose:** Security teams need a guide for using the dashboard; API consumers
  need endpoint reference
- **Reference:** Feature TC-9006

## Acceptance Criteria
- [ ] API endpoint documentation covers `GET /api/v2/remediation/summary` with request/response examples
- [ ] API endpoint documentation covers `GET /api/v2/remediation/by-product` with pagination parameters and response examples
- [ ] Dashboard user guide explains how to navigate to `/remediation`, interpret summary cards, and use the progress chart
- [ ] Filter documentation explains how to filter the vulnerability table by severity, product, and status
- [ ] Documentation is consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify API endpoint documentation examples match the actual response shapes from the backend
- [ ] Verify dashboard screenshots or descriptions match the current UI implementation
- [ ] Verify filter descriptions match the available filter options in the UI

## Dependencies
- Depends on: Task 2 — Add remediation summary and by-product REST endpoints
- Depends on: Task 5 — Add remediation dashboard page with summary cards and progress chart
- Depends on: Task 6 — Add filterable vulnerability table to remediation dashboard

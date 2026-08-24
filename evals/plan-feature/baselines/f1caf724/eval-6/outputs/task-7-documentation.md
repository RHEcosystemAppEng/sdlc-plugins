## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Document the new remediation tracking dashboard and aggregation API endpoints. The feature introduces two new backend endpoints (`GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`) and a frontend dashboard page at `/remediation`.

Documentation scope (from Feature Documentation Considerations):
- **Doc impact type:** New Content
- **User purpose:** Security teams need a guide for using the remediation dashboard to monitor portfolio-wide remediation progress. API consumers need endpoint reference documentation for the summary and by-product aggregation endpoints.
- **Content to cover:**
  - Dashboard usage guide: navigating to `/remediation`, interpreting summary cards, reading the progress chart, using filters in the vulnerability table
  - API endpoint reference: request/response shapes, query parameters, pagination, error responses for both remediation endpoints
  - Use case examples aligned with UC-1 (view remediation summary) and UC-2 (filter by product)

## Acceptance Criteria
- [ ] Dashboard usage guide documents how to navigate to and use the remediation dashboard
- [ ] API endpoint reference documents `GET /api/v2/remediation/summary` with request/response shapes
- [ ] API endpoint reference documents `GET /api/v2/remediation/by-product` with pagination parameters and response shape
- [ ] Documentation accurately reflects the implemented feature behavior
- [ ] Documentation covers the scope identified in the Feature's Documentation Considerations section

## Test Requirements
- [ ] Verify API endpoint documentation matches actual endpoint behavior (request parameters, response shapes)
- [ ] Verify dashboard usage guide accurately describes the UI components and user workflows
- [ ] Verify documentation is consistent with the implemented acceptance criteria from Tasks 1-6

## Dependencies
- Depends on: Task 1 — Add remediation module with summary aggregation endpoint
- Depends on: Task 2 — Add remediation by-product aggregation endpoint
- Depends on: Task 3 — Add remediation endpoint integration tests
- Depends on: Task 4 — Add remediation API client, TypeScript models, and React Query hooks
- Depends on: Task 5 — Add remediation dashboard page with summary cards and progress chart
- Depends on: Task 6 — Add filterable vulnerability table to remediation dashboard

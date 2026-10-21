## Repository
trustify-backend

## Parent Epic
TC-9007 (TC-9006: trustify-backend)

## Target Branch
main

## Description
Document the new vulnerability remediation tracking dashboard and its backend aggregation API endpoints. The Feature description (TC-9006) indicates a "New Content" documentation impact. Security teams need a user guide for the remediation dashboard, and API consumers need an endpoint reference for `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`.

Documentation scope:
- **API reference**: document both new remediation endpoints with request parameters, response shapes, and example responses
- **Dashboard user guide**: document the remediation dashboard UI including summary cards, progress chart, filterable vulnerability table, and filter/sort capabilities
- **Use case walkthroughs**: document UC-1 (View remediation summary) and UC-2 (Filter by product) from the Feature description

## Acceptance Criteria
- [ ] API reference documents `GET /api/v2/remediation/summary` with response shape and example
- [ ] API reference documents `GET /api/v2/remediation/by-product` with pagination parameters and response shape
- [ ] Dashboard user guide covers summary cards (Open, In Progress, Resolved counts)
- [ ] Dashboard user guide covers progress chart (30-day remediation trend)
- [ ] Dashboard user guide covers filterable vulnerability table with severity, product, and status filters
- [ ] Documentation accurately reflects the implemented feature behavior
- [ ] Documentation covers the full scope identified in the Feature's Documentation Considerations section

## Test Requirements
- [ ] API endpoint descriptions match actual request parameters and response shapes from the implementation
- [ ] Dashboard usage instructions match the actual UI behavior and component layout
- [ ] Example API responses are valid and representative
- [ ] All documented filter options (severity, product, status) match the implemented filters

## Dependencies
- Depends on: Task 1 -- Add remediation data models and aggregation service
- Depends on: Task 2 -- Add remediation summary and by-product endpoints
- Depends on: Task 3 -- Add integration tests for remediation endpoints
- Depends on: Task 4 -- Add remediation API types, client functions, and React Query hooks
- Depends on: Task 5 -- Add RemediationDashboardPage with summary cards and progress chart
- Depends on: Task 6 -- Add filterable vulnerability table to remediation dashboard
- Depends on: Task 7 -- Add route registration, navigation, and tests for remediation dashboard

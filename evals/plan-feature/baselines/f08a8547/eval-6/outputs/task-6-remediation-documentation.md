## Repository
trustify-ui

## Target Branch
main

## Description
Document the new vulnerability remediation tracking dashboard and aggregation API endpoints. The Feature's Documentation Considerations specify "New Content" doc impact — new documentation pages or sections are needed. Security teams need a user guide for navigating and using the remediation dashboard, and API consumers need an endpoint reference for the remediation aggregation APIs (GET /api/v2/remediation/summary and GET /api/v2/remediation/by-product). Reference Feature issue TC-9006 for full requirements context.

## Acceptance Criteria
- [ ] Dashboard user guide documents navigation to the /remediation page
- [ ] User guide describes summary cards (Open, In Progress, Resolved counts)
- [ ] User guide describes the progress chart showing remediation trend over 30 days
- [ ] User guide describes the filterable vulnerability table with severity, product, and status filters
- [ ] API endpoint reference documents GET /api/v2/remediation/summary with request parameters and response shape
- [ ] API endpoint reference documents GET /api/v2/remediation/by-product with pagination parameters and response shape
- [ ] Documentation references Feature issue TC-9006

## Test Requirements
- [ ] Documentation accurately reflects the implemented dashboard behavior and UI components
- [ ] API endpoint reference matches the actual request/response contracts from the backend
- [ ] Documentation is complete and covers all MVP requirements from the Feature description

## Dependencies
- Depends on: Task 1 — Create remediation module with summary aggregation endpoint
- Depends on: Task 2 — Add per-product remediation breakdown endpoint
- Depends on: Task 3 — Add remediation API types, client functions, and React Query hooks
- Depends on: Task 4 — Create remediation dashboard page with summary cards and progress chart
- Depends on: Task 5 — Add filterable vulnerability table to remediation dashboard

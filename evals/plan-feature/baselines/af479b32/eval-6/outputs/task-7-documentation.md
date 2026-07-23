## Repository
trustify-backend

## Target Branch
main

## Description
Create documentation for the vulnerability remediation tracking dashboard feature (TC-9006). The Feature's Documentation Considerations section indicates "New Content" is required with the following scope:

- **Doc impact type:** New Content
- **User purpose:** Security teams need a guide for using the remediation dashboard; API consumers need endpoint reference documentation
- **Scope:** Document the remediation dashboard page (/remediation), including summary cards, progress chart, and filterable vulnerability table. Document the aggregation API endpoints (GET /api/v2/remediation/summary, GET /api/v2/remediation/by-product, GET /api/v2/remediation/export) with request/response schemas and usage examples.

Reference feature: TC-9006 (Add vulnerability remediation tracking dashboard)

## Acceptance Criteria
- [ ] API endpoint reference documentation covers GET /api/v2/remediation/summary with request parameters and response schema
- [ ] API endpoint reference documentation covers GET /api/v2/remediation/by-product with pagination parameters and response schema
- [ ] API endpoint reference documentation covers GET /api/v2/remediation/export with response format description
- [ ] User guide documentation describes how to navigate to and use the remediation dashboard
- [ ] User guide covers the summary cards, progress chart, and filterable table functionality
- [ ] User guide covers filtering by severity, product, and status
- [ ] Documentation accurately reflects the implemented feature behavior

## Test Requirements
- [ ] Verify all documented API endpoints match the actual endpoint paths and response shapes
- [ ] Verify documented filter options match the implemented filter categories
- [ ] Verify the user guide's described workflow matches the actual UI behavior

## Dependencies
- Depends on: Task 1 — Create remediation module with summary endpoint
- Depends on: Task 2 — Add GET /api/v2/remediation/by-product endpoint
- Depends on: Task 3 — Add remediation API types, client functions, and React Query hooks
- Depends on: Task 4 — Create remediation dashboard page with summary cards and progress chart
- Depends on: Task 5 — Add filterable vulnerability table to remediation dashboard
- Depends on: Task 6 — Add CSV export for remediation report

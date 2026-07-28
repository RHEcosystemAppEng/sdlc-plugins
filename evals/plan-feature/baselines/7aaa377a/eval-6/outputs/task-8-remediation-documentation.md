## Repository
trustify-backend

## Target Branch
main

## Description
Document the remediation dashboard feature and aggregation API endpoints. The Feature's Documentation Considerations section indicates "New Content" doc impact: security teams need a guide for using the dashboard, and API consumers need endpoint reference documentation. Documentation should cover the remediation dashboard user workflow, the aggregation API endpoints (GET /api/v2/remediation/summary and GET /api/v2/remediation/by-product), request/response formats, filtering capabilities, and use cases for security managers and engineering leads.

See Feature TC-9006 for the full feature specification and use cases.

## Acceptance Criteria
- [ ] API endpoint reference documents GET /api/v2/remediation/summary with request parameters, response shape, and example response
- [ ] API endpoint reference documents GET /api/v2/remediation/by-product with pagination parameters, response shape, and example response
- [ ] Dashboard user guide covers navigating to /remediation and interpreting summary cards
- [ ] Dashboard user guide covers using filters (severity, product, status) to drill down into data
- [ ] Documentation covers both use cases: UC-1 (view remediation summary) and UC-2 (filter by product)

## Test Requirements
- [ ] Documentation accurately reflects the implemented API response shapes
- [ ] Documentation accurately describes the dashboard UI components and filter behavior
- [ ] Documentation is consistent with the feature specification in TC-9006

## Dependencies
- Depends on: Task 1 -- Add remediation summary aggregation endpoint
- Depends on: Task 2 -- Add per-product remediation breakdown endpoint
- Depends on: Task 3 -- Add integration tests for remediation endpoints
- Depends on: Task 4 -- Add API types and React Query hooks for remediation endpoints
- Depends on: Task 5 -- Create remediation dashboard page with summary cards and progress chart
- Depends on: Task 6 -- Add filterable vulnerability table to remediation dashboard
- Depends on: Task 7 -- Add unit and E2E tests for remediation dashboard

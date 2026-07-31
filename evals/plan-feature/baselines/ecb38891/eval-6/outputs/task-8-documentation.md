# Task 8: Document remediation dashboard and aggregation endpoints

## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Create documentation for the new vulnerability remediation tracking dashboard and its backend aggregation endpoints. The Feature's Documentation Considerations section indicates New Content is needed: security teams need a user guide for the dashboard, and API consumers need endpoint reference documentation.

Documentation scope:
- **New Content**: user guide for the remediation dashboard page, covering navigation, summary cards, progress chart, and filterable vulnerability table
- **New Content**: API reference for `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product` endpoints, including request parameters and response shapes
- **User purpose**: Security managers tracking remediation SLAs, engineering leads prioritizing fix work, API consumers building integrations

Reference: Feature TC-9006 -- Add vulnerability remediation tracking dashboard

## Acceptance Criteria
- [ ] User guide documents how to navigate to and use the remediation dashboard
- [ ] User guide covers summary cards (Open, In Progress, Resolved counts) and how to interpret them
- [ ] User guide covers the progress chart and what it displays (30-day trend)
- [ ] User guide covers the filterable vulnerability table with instructions for filtering by severity, product, and status
- [ ] API reference documents `GET /api/v2/remediation/summary` endpoint with request parameters and response shape
- [ ] API reference documents `GET /api/v2/remediation/by-product` endpoint with request parameters and response shape
- [ ] Documentation is accurate and consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify documentation accurately reflects the dashboard's actual UI components and behavior
- [ ] Verify API endpoint documentation matches the actual request/response shapes
- [ ] Verify all filter options (severity, product, status) are documented
- [ ] Verify documentation covers both use cases: UC-1 (view remediation summary) and UC-2 (filter by product)

## Dependencies
- Depends on: Task 2 -- Add remediation aggregation service and API endpoints
- Depends on: Task 3 -- Add integration tests for remediation endpoints
- Depends on: Task 4 -- Add remediation API types, client functions, and React Query hooks
- Depends on: Task 5 -- Create RemediationDashboardPage with summary cards and progress chart
- Depends on: Task 6 -- Add filterable vulnerability table to remediation dashboard
- Depends on: Task 7 -- Add E2E tests for remediation dashboard

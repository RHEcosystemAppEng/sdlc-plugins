# Task 10: Document remediation dashboard and API endpoints

**Epic:** TC-9006: trustify-ui

## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Create documentation for the vulnerability remediation tracking dashboard and the supporting backend aggregation API endpoints. The Feature description indicates a "New Content" documentation impact: security teams need a guide for using the dashboard, and API consumers need an endpoint reference for the remediation aggregation APIs.

Documentation should cover:
- **Dashboard user guide**: how to navigate to the remediation dashboard, interpret summary cards and progress charts, use filters to drill down by severity/product/status
- **API endpoint reference**: request/response format for `GET /api/v2/remediation/summary`, `GET /api/v2/remediation/by-product`, and `GET /api/v2/remediation/export`
- **Use cases**: walkthrough of UC-1 (View remediation summary) and UC-2 (Filter by product)

## Acceptance Criteria
- [ ] Dashboard user guide documents navigation, summary cards, progress chart, and filterable table
- [ ] API endpoint reference documents all three remediation endpoints with request/response formats
- [ ] Use case walkthroughs cover UC-1 and UC-2 from the feature description
- [ ] Documentation accurately reflects the implemented feature behavior

## Test Requirements
- [ ] Verify documentation is accurate by comparing against actual dashboard behavior
- [ ] Verify API endpoint documentation matches actual request/response shapes
- [ ] Verify all screenshots or examples reflect the current implementation

## Dependencies
- Depends on: Task 2 — Add remediation summary endpoint
- Depends on: Task 3 — Add remediation by-product endpoint
- Depends on: Task 5 — Add remediation API types, client functions, and hooks
- Depends on: Task 6 — Create remediation dashboard page with summary cards and progress chart
- Depends on: Task 7 — Add filterable vulnerability table to remediation dashboard
- Depends on: Task 8 — Register remediation route and navigation
- Depends on: Task 9 — Add CSV export endpoint for remediation data

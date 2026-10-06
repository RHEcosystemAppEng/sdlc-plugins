## Repository
trustify-backend

## Target Branch
main

## Description
Document the vulnerability remediation tracking dashboard feature including the new aggregation API endpoints and the frontend dashboard usage guide. The Feature description identifies this as New Content: security teams need a guide for using the dashboard, and API consumers need endpoint reference documentation.

Documentation should cover:
- API reference for `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product` endpoints (request parameters, response schemas, example responses)
- Dashboard usage guide explaining how to navigate the remediation dashboard, interpret summary cards, read the progress chart, and use filters
- Use case walkthroughs for UC-1 (view remediation summary) and UC-2 (filter by product)

Reference: Feature TC-9006 -- Add vulnerability remediation tracking dashboard

## Acceptance Criteria
- [ ] API reference documents both remediation endpoints with request/response schemas and example payloads
- [ ] Dashboard usage guide explains the summary cards, progress chart, and filterable table
- [ ] Documentation covers the two primary use cases (UC-1: view remediation summary, UC-2: filter by product)
- [ ] Documentation accurately reflects the implemented feature behavior
- [ ] Documentation covers the scope identified in the Feature's Documentation Considerations (New Content for security teams and API consumers)

## Test Requirements
- [ ] Review documentation against implemented API response shapes for accuracy
- [ ] Verify example API responses match actual endpoint output
- [ ] Verify dashboard screenshots or descriptions match the implemented UI

## Dependencies
- Depends on: Task 1 -- Add remediation data models and aggregation service
- Depends on: Task 2 -- Add remediation summary endpoint
- Depends on: Task 3 -- Add remediation by-product endpoint
- Depends on: Task 4 -- Add integration tests for remediation endpoints
- Depends on: Task 5 -- Add API client and React Query hooks for remediation endpoints
- Depends on: Task 6 -- Add remediation dashboard page with summary cards and progress chart
- Depends on: Task 7 -- Add filterable vulnerability table to remediation dashboard
- Depends on: Task 8 -- Add tests for remediation dashboard page

## Parent Epic
TC-9007

## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Document the vulnerability remediation tracking dashboard and the backend aggregation API endpoints introduced by TC-9006. The Feature's Documentation Considerations indicate **New Content** is needed: security teams need a guide for using the remediation dashboard, and API consumers need an endpoint reference for the three new remediation endpoints (`/api/v2/remediation/summary`, `/api/v2/remediation/by-product`, `/api/v2/remediation/export`).

Doc impact type: **New Content**

Documentation scope:
- User guide for the remediation dashboard page at `/remediation`: summary cards, progress chart, filterable vulnerability table, and CSV export
- API reference for the three new remediation endpoints with request parameters, response shapes, and example responses
- Reference to TC-9006 for feature context

## Acceptance Criteria
- [ ] User guide documents the remediation dashboard page: navigation, summary cards, progress chart, filterable table, and CSV export
- [ ] API reference documents `GET /api/v2/remediation/summary` with response shape and example
- [ ] API reference documents `GET /api/v2/remediation/by-product` with pagination parameters and response shape
- [ ] API reference documents `GET /api/v2/remediation/export` with CSV format description
- [ ] Documentation accurately reflects the implemented feature behavior

## Test Requirements
- [ ] Verify documentation content matches the actual dashboard layout and behavior
- [ ] Verify API endpoint documentation matches actual request/response shapes
- [ ] Verify all navigation paths described in the documentation are accurate

## Dependencies
- Depends on: Task 2 — Add remediation summary aggregation service and endpoint
- Depends on: Task 3 — Add per-product remediation breakdown endpoint
- Depends on: Task 4 — Add CSV export endpoint for remediation report
- Depends on: Task 5 — Add API client functions, types, and React Query hooks for remediation endpoints
- Depends on: Task 6 — Add remediation dashboard page with summary cards and progress chart
- Depends on: Task 7 — Add filterable vulnerability table to remediation dashboard
- Depends on: Task 8 — Add CSV export button to remediation dashboard

## Repository
trustify-backend

## Target Branch
main

## Description
Document the TC-9006 vulnerability remediation tracking feature.

**What changed:** a new remediation dashboard page at `/remediation` (summary cards for Open / In Progress / Resolved, a 30-day remediation trend chart, and a vulnerability table filterable by severity, product, and status) backed by new aggregation endpoints `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`, plus the supporting `GET /api/v2/remediation/vulnerabilities` and `GET /api/v2/remediation/trend` endpoints.

**Doc impact type:** New Content.

**Details from Documentation Considerations:** document the remediation dashboard and the aggregation endpoints. User purpose: security teams need a guide for using the dashboard; API consumers need an endpoint reference (paths, query parameters, response shapes, pagination of the by-product breakdown for portfolios >50 products). Note the customer consideration that remediation status depends on advisory correlation being up to date.

Reference: Feature TC-9006 — Add vulnerability remediation tracking dashboard.

Assumption: no dedicated documentation repository is listed in the Repository Registry, so this task is placed in trustify-backend (which hosts the API reference). The dashboard user guide content may be cross-linked from trustify-ui's README by the implementer.

## Acceptance Criteria
- [ ] Endpoint reference covers all four `/api/v2/remediation/*` endpoints with query parameters, response shapes, and pagination behavior, and matches the implemented behavior
- [ ] A user guide section explains how to use the `/remediation` dashboard: summary cards, trend chart, and filtering/sorting the vulnerability table (UC-1 and UC-2)
- [ ] Documentation states that remediation status relies on up-to-date advisory correlation

## Test Requirements
- [ ] Verify every documented endpoint path, parameter, and response field against the merged backend implementation
- [ ] Walk through UC-1 and UC-2 against a running instance following only the documentation and confirm the steps are accurate and complete
- [ ] Verify documentation is consistent with the UI labels (Open / In Progress / Resolved, severity names)

## Dependencies
- Depends on: Task 2 — Add remediation summary and by-product endpoints
- Depends on: Task 3 — Add remediation vulnerabilities list and trend endpoints
- Depends on: Task 5 — Create remediation dashboard page with summary cards and trend chart
- Depends on: Task 6 — Add filterable vulnerability table to the remediation dashboard

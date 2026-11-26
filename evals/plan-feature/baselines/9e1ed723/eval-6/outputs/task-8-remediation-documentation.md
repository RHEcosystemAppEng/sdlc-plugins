# Task 8 — Document the remediation dashboard and aggregation endpoints

**Summary:** Document the remediation tracking dashboard and remediation API endpoints
**Parent Epic:** TC-9006: trustify-backend (Epic group "trustify-backend")

## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Write the documentation for TC-9006 (Add vulnerability remediation tracking dashboard).

**What changed:** a portfolio-wide vulnerability remediation tracking dashboard at `/remediation` in trustify-ui, with summary cards (Open / In Progress / Resolved), a status-by-severity progress chart, and a vulnerability table filterable by severity, product, and status. It is backed by new trustify-backend endpoints: `GET /api/v2/remediation/summary`, `GET /api/v2/remediation/by-product`, and `GET /api/v2/remediation/vulnerabilities`.

**Doc impact type:** New Content

**Details from Documentation Considerations:**
- Document the remediation dashboard and the aggregation endpoints
- User purpose: security teams need a guide for using the dashboard, and API consumers need an endpoint reference
- Include the customer considerations: remediation status depends on advisory correlation being up to date, and the product breakdown is paginated for large portfolios (>50 products)

Reference: Feature TC-9006.

## Acceptance Criteria
- [ ] Documentation gives an endpoint reference for the three remediation endpoints (paths, query parameters, response shapes, pagination) that matches the implemented behavior
- [ ] Documentation includes a user guide for the `/remediation` dashboard covering the summary cards, the progress chart, and filtering by severity, product, and status (UC-1 and UC-2)
- [ ] Documentation states that remediation status depends on up-to-date advisory correlation
- [ ] Documentation does not describe excluded functionality (30-day trend, CSV export) as available

## Test Requirements
- [ ] Check every documented endpoint, parameter, and response field against the implemented code on the `TC-9006` branch
- [ ] Walk through the user-guide steps against a running dashboard and confirm they are accurate and complete
- [ ] Confirm consistent terminology (Open / In Progress / Resolved; Critical/High/Medium/Low) between the docs, the UI labels, and the API values

## Dependencies
- Depends on: Task 2 — Add remediation module and GET /api/v2/remediation/summary endpoint
- Depends on: Task 3 — Add GET /api/v2/remediation/by-product endpoint
- Depends on: Task 4 — Add filterable GET /api/v2/remediation/vulnerabilities list endpoint
- Depends on: Task 5 — Add remediation API client functions, models, and React Query hooks
- Depends on: Task 6 — Add /remediation dashboard page with summary cards and progress chart
- Depends on: Task 7 — Add filterable vulnerability table to the remediation dashboard

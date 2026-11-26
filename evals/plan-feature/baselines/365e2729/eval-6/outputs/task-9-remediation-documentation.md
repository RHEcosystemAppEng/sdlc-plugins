# Task 9 — Document remediation dashboard and aggregation endpoints

**Parent Epic:** TC-9006: trustify-backend (<EPIC-BE>)
**Issue type:** Task
**Labels:** ai-generated-jira
**Priority:** Major
**fixVersions:** RHTPA 1.5.0

---

## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Write documentation for TC-9006 (Add vulnerability remediation tracking dashboard).

**What changed:** the backend adds three aggregation endpoints:
- `GET /api/v2/remediation/summary`, which returns counts by severity × status
- `GET /api/v2/remediation/by-product`, which returns a paginated per-product breakdown
- `GET /api/v2/remediation/vulnerabilities`, which returns a filterable, paginated list

The UI adds a `/remediation` dashboard with Open/In Progress/Resolved summary cards, a progress chart, and a filterable vulnerability table (filters: severity, product, status).

**Doc impact type:** New Content.

**Details from Documentation Considerations:**
- Document the remediation dashboard and the aggregation endpoints.
- User purpose: security teams need a guide for using the dashboard, and API consumers need an endpoint reference.
- Note the dependency from Customer Considerations: remediation status depends on up-to-date advisory correlation. Also note that the 30-day trend view and CSV export are not part of this release.

Reference: TC-9006.

## Acceptance Criteria
- [ ] The API reference documents all three remediation endpoints, including paths, query parameters (filters, pagination, sort), response shapes, and error responses (400 for invalid filters)
- [ ] The user guide explains how to use the `/remediation` dashboard: what the summary cards and progress chart show, and how to filter the table by severity, product, and status and sort by severity (UC-1, UC-2)
- [ ] The documentation states that counts depend on advisory correlation being current
- [ ] The documentation matches the implemented behavior (field names, status labels, counting semantics)

## Test Requirements
- [ ] Every documented endpoint example request is run against the `TC-9006` build, and the response matches the documented shape
- [ ] The dashboard walkthrough steps are checked against the running UI
- [ ] The documented filter values and status labels match the API and UI exactly

## Dependencies
- Depends on: Task 2 — Add remediation module and GET /api/v2/remediation/summary
- Depends on: Task 3 — Add GET /api/v2/remediation/by-product
- Depends on: Task 4 — Add GET /api/v2/remediation/vulnerabilities (filterable list)
- Depends on: Task 6 — Add remediation API models, REST functions and React Query hooks
- Depends on: Task 7 — Add /remediation dashboard page with summary cards and progress chart
- Depends on: Task 8 — Add filterable vulnerability table to remediation dashboard

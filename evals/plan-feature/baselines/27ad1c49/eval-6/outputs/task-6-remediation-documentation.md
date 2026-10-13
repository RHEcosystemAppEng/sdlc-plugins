## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9006: trustify-ui

## Description
Document the remediation dashboard feature for end users and API consumers. Create a user guide explaining how to use the remediation dashboard (navigating to the page, interpreting summary cards, reading the progress chart, using filters) and an API reference section for the two new backend endpoints (`GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`) including request parameters and response schemas.

## Acceptance Criteria
- [ ] User guide documents how to navigate to the remediation dashboard
- [ ] User guide explains the summary cards (Open, In Progress, Resolved counts with severity breakdown)
- [ ] User guide explains the progress chart (30-day remediation trend)
- [ ] User guide explains how to use filters (severity, product, status) on the vulnerability table
- [ ] API reference documents `GET /api/v2/remediation/summary` with response schema and example
- [ ] API reference documents `GET /api/v2/remediation/by-product` with query parameters (pagination, filters) and response schema
- [ ] Documentation follows existing documentation conventions and structure

## Test Requirements
- [ ] Documentation reviewed for accuracy against implemented dashboard behavior
- [ ] API examples verified against actual endpoint responses

## Dependencies
- Depends on: Task 4 — Build remediation dashboard page with summary cards and progress chart
- Depends on: Task 5 — Add filterable vulnerability table to remediation dashboard

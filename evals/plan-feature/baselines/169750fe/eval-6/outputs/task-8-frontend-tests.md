## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9006: trustify-ui

## Description
Add MSW request handlers for the remediation API endpoints, mock fixtures, and comprehensive component tests for the remediation dashboard page and its sub-components.

## Files to Create
- `tests/mocks/fixtures/remediation-summary.json` — mock remediation summary data
- `tests/mocks/fixtures/remediation-by-product.json` — mock per-product remediation data

## Files to Modify
- `tests/mocks/handlers.ts` — add MSW handlers for GET /api/v2/remediation/summary and GET /api/v2/remediation/by-product

## Implementation Notes
- Follow the MSW handler pattern in `tests/mocks/handlers.ts` — add handlers for both remediation endpoints.
- Create fixture files in `tests/mocks/fixtures/` matching the patterns in `tests/mocks/fixtures/sboms.json` and `tests/mocks/fixtures/advisories.json`.
- Per Key Conventions: Vitest + React Testing Library for unit tests; MSW for API mocking.
Applies: task modifies `tests/mocks/handlers.ts` matching the convention's testing scope.
- The `remediation-summary.json` fixture should include counts across all severity × status combinations.
- The `remediation-by-product.json` fixture should include multiple products with varying remediation states.
- Tests for `RemediationDashboardPage` should verify rendering of summary cards, chart, and table using the mock data.

## Reuse Candidates
- `tests/mocks/handlers.ts` — existing MSW handler patterns
- `tests/mocks/fixtures/sboms.json` — example fixture file structure
- `tests/setup.ts` — test setup with MSW handlers and render helpers

## Acceptance Criteria
- [ ] MSW handlers intercept both remediation endpoints and return fixture data
- [ ] Fixture files contain representative remediation data
- [ ] Tests verify summary cards render correct counts
- [ ] Tests verify filter interactions update table content
- [ ] Tests verify loading and empty states

## Test Requirements
- [ ] MSW handlers return correct fixture data for both endpoints
- [ ] At least one test per dashboard sub-component (SummaryCards, RemediationChart, VulnerabilityTable)
- [ ] Integration test for the full dashboard page rendering

## Dependencies
- Depends on: Task 7 — Remediation dashboard page

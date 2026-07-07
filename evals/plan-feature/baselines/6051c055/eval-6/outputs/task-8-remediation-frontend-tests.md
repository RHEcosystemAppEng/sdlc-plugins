## Repository
trustify-ui

## Target Branch
main

## Description
Add comprehensive unit and end-to-end tests for the remediation dashboard (TC-9006). This includes Vitest + React Testing Library unit tests for the dashboard page and its components, MSW mock handlers for the remediation API endpoints, mock fixtures, and Playwright E2E tests that verify the full user workflow.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — unit tests for the dashboard page, summary cards, filters, and table
- `tests/mocks/fixtures/remediation.json` — mock remediation data (summary and by-product responses)
- `tests/e2e/remediation-dashboard.spec.ts` — Playwright E2E tests for UC-1 and UC-2 user flows

## Files to Modify
- `tests/mocks/handlers.ts` — add MSW request handlers for GET /api/v2/remediation/summary and GET /api/v2/remediation/by-product

## Implementation Notes
- Follow the existing test patterns:
  - Unit tests use Vitest + React Testing Library, as seen in `src/pages/SbomListPage/SbomListPage.test.tsx` and `src/pages/AdvisoryListPage/AdvisoryListPage.test.tsx`.
  - MSW handlers follow the pattern in `tests/mocks/handlers.ts` for intercepting API requests.
  - Mock fixtures follow the JSON format in `tests/mocks/fixtures/sboms.json` and `tests/mocks/fixtures/advisories.json`.
  - E2E tests use Playwright, following the pattern in `tests/e2e/sbom-list.spec.ts`.
- Unit tests should cover:
  - Summary cards rendering with correct counts
  - Progress chart rendering with trend data
  - Filter toolbar interaction (applying severity, product, status filters)
  - Vulnerability table rendering with mock data
  - Loading and empty states
- E2E tests should cover the two use cases from the feature:
  - UC-1: Navigate to /remediation, verify summary cards and chart load, verify table shows outstanding vulnerabilities
  - UC-2: Select a product filter, verify dashboard updates to show only that product's vulnerabilities

Per CONVENTIONS.md Section "Testing": Vitest + React Testing Library for unit tests; Playwright for E2E; MSW for API mocking.
Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` matching the convention's `.test.tsx` test file scope.

Per CONVENTIONS.md Section "Naming": camelCase for utilities, kebab-case for directories.
Applies: task creates `tests/e2e/remediation-dashboard.spec.ts` matching the convention's `.spec.ts` test file scope.

## Reuse Candidates
- `tests/setup.ts` — test setup with MSW handlers and render helpers; import for unit test setup
- `tests/mocks/handlers.ts` — existing MSW handler patterns to follow for adding remediation handlers
- `tests/mocks/fixtures/sboms.json` — reference for mock fixture JSON format
- `src/pages/SbomListPage/SbomListPage.test.tsx` — reference for page-level unit test patterns with data fetching
- `tests/e2e/sbom-list.spec.ts` — reference for Playwright E2E test patterns

## Acceptance Criteria
- [ ] Unit tests verify summary cards render correct Open, In Progress, Resolved counts
- [ ] Unit tests verify progress chart renders with trend data
- [ ] Unit tests verify filter interactions update the vulnerability table
- [ ] Unit tests verify loading and empty states
- [ ] MSW handlers intercept remediation API requests and return mock data
- [ ] E2E test covers UC-1: full dashboard loading and vulnerability review
- [ ] E2E test covers UC-2: product filter selection and dashboard update

## Test Requirements
- [ ] All unit tests pass with `npx vitest run`
- [ ] E2E tests pass with `npx playwright test tests/e2e/remediation-dashboard.spec.ts`
- [ ] MSW handlers return appropriate mock data for both remediation endpoints
- [ ] Mock fixture data includes multiple products, severities, and statuses for comprehensive testing

## Verification Commands
- `npx vitest run src/pages/RemediationDashboardPage/` — unit tests pass
- `npx playwright test tests/e2e/remediation-dashboard.spec.ts` — E2E tests pass

## Dependencies
- Depends on: Task 5 — Create remediation dashboard page with summary cards and progress chart
- Depends on: Task 6 — Add filterable vulnerability table to remediation dashboard
- Depends on: Task 7 — Register remediation dashboard route and add navigation entry

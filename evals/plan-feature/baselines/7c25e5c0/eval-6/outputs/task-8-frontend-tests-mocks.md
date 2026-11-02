## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9006: trustify-ui

## Description
Add MSW mock handlers, test fixtures, and unit tests for the remediation dashboard. This includes mock API handlers for both remediation endpoints, fixture data matching the backend response shapes, and component tests for the dashboard page and its sub-components.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — unit tests for the dashboard page component
- `tests/mocks/fixtures/remediation-summary.json` — mock data for remediation summary endpoint
- `tests/mocks/fixtures/remediation-by-product.json` — mock data for remediation by-product endpoint

## Files to Modify
- `tests/mocks/handlers.ts` — add MSW request handlers for GET /api/v2/remediation/summary and GET /api/v2/remediation/by-product

## Implementation Notes
Follow existing test and mock patterns:

- **MSW handlers**: `tests/mocks/handlers.ts` — add `rest.get('/api/v2/remediation/summary', ...)` and `rest.get('/api/v2/remediation/by-product', ...)` handlers following the pattern of existing handlers for SBOM and advisory endpoints
- **Fixture data**: `tests/mocks/fixtures/sboms.json` and `tests/mocks/fixtures/advisories.json` — follow the same JSON structure pattern for remediation fixtures
- **Component tests**: `src/pages/SbomListPage/SbomListPage.test.tsx` — follow the same test structure: render component, wait for data to load, assert on rendered content
- **Test utilities**: use the render helpers and setup from `tests/setup.ts`
- **Testing framework**: Vitest + React Testing Library (not Jest)

Test scenarios for RemediationDashboardPage:
1. Renders summary cards with correct counts from mocked data
2. Renders filterable table with vulnerability entries
3. Filtering by severity updates displayed rows
4. Filtering by product updates displayed rows
5. Empty state when no remediation data exists
6. Loading spinner shown during data fetch

## Acceptance Criteria
- [ ] MSW handlers intercept GET /api/v2/remediation/summary and return fixture data
- [ ] MSW handlers intercept GET /api/v2/remediation/by-product and return fixture data
- [ ] Component tests verify summary cards render with correct counts
- [ ] Component tests verify table renders vulnerability data
- [ ] Component tests verify filter interactions
- [ ] All tests pass with `vitest run`

## Test Requirements
- [ ] At least 6 test cases covering: summary card rendering, table rendering, severity filter, product filter, empty state, loading state
- [ ] Tests use MSW mock handlers — no direct API calls
- [ ] Fixture data matches backend response shapes defined in Task 5 interfaces
- [ ] Tests follow React Testing Library best practices (query by role/text, not implementation details)

## Dependencies
- Depends on: Task 7 — Remediation dashboard page

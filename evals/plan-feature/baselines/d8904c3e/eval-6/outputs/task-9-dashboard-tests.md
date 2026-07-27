## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Add comprehensive unit tests, MSW mock handlers, and Playwright E2E tests for the remediation dashboard page and its components. This ensures the dashboard renders correctly, filters work as expected, and the full user flow from navigation to data display functions properly.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` -- unit tests using Vitest + React Testing Library for the dashboard page, summary cards, progress chart, and vulnerability table
- `tests/mocks/fixtures/remediation.json` -- mock remediation data (summary and by-product responses) for MSW handlers
- `tests/e2e/remediation-dashboard.spec.ts` -- Playwright E2E test: navigate to /remediation, verify summary cards load, verify table renders, test filter interactions

## Files to Modify
- `tests/mocks/handlers.ts` -- add MSW request handlers for GET /api/v2/remediation/summary and GET /api/v2/remediation/by-product returning mock fixture data

## Implementation Notes
- Follow the testing patterns from `src/pages/SbomListPage/SbomListPage.test.tsx` for unit tests: use Vitest + React Testing Library with MSW for API mocking.
  Per CONVENTIONS.md: Vitest + React Testing Library for unit tests; Playwright for E2E; MSW for API mocking.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` matching the convention's TypeScript test file scope.
- Follow the E2E test patterns from `tests/e2e/sbom-list.spec.ts` for Playwright tests.
  Per CONVENTIONS.md: Playwright for E2E tests.
  Applies: task creates `tests/e2e/remediation-dashboard.spec.ts` matching the convention's TypeScript E2E test file scope.
- Follow MSW handler patterns from `tests/mocks/handlers.ts` for adding new API mock handlers.
  Per CONVENTIONS.md: MSW for API mocking with handlers in tests/mocks/handlers.ts.
  Applies: task modifies `tests/mocks/handlers.ts` matching the convention's TypeScript file scope.
- Follow fixture patterns from `tests/mocks/fixtures/sboms.json` and `tests/mocks/fixtures/advisories.json` for mock data structure.
- Use the test setup from `tests/setup.ts` which provides render helpers and MSW server configuration.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.test.tsx` -- SBOM list page unit tests; follow as template for component testing patterns
- `tests/e2e/sbom-list.spec.ts` -- Playwright E2E test; follow as template for E2E test structure
- `tests/mocks/handlers.ts` -- existing MSW handlers; extend with remediation endpoint handlers
- `tests/mocks/fixtures/sboms.json` -- mock SBOM data fixture; follow structure for remediation fixtures
- `tests/setup.ts` -- test setup with render helpers; reuse for test configuration

## Acceptance Criteria
- [ ] Unit tests verify summary cards render correct Open, In Progress, and Resolved counts
- [ ] Unit tests verify progress chart renders without errors
- [ ] Unit tests verify vulnerability table renders with correct data
- [ ] Unit tests verify filter interactions (severity, product, status) update the table
- [ ] Unit tests verify loading and empty states
- [ ] MSW handlers return mock remediation data for both endpoints
- [ ] E2E test navigates to /remediation and verifies dashboard loads
- [ ] E2E test interacts with filters and verifies table updates
- [ ] All tests pass

## Test Requirements
- [ ] Unit test: RemediationDashboardPage renders summary cards with mocked summary data
- [ ] Unit test: RemediationDashboardPage renders progress chart
- [ ] Unit test: VulnerabilityTable renders rows from mocked by-product data
- [ ] Unit test: severity filter updates table content
- [ ] Unit test: product filter updates table content
- [ ] Unit test: status filter updates table content
- [ ] Unit test: loading state shows spinner
- [ ] Unit test: empty state shows empty card
- [ ] E2E test: full navigation and interaction flow

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9006 from main
- Depends on: Task 7 -- Add remediation dashboard page with summary cards, progress chart, and route registration
- Depends on: Task 8 -- Add filterable vulnerability table to remediation dashboard

## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9006: trustify-ui

## Description
Register the `/remediation` route in the application router, add the remediation dashboard as a lazy-loaded page component, and add comprehensive test coverage. This includes MSW mock handlers for the remediation API endpoints, fixture data, unit tests for the dashboard page and its components, and a Playwright E2E test for the full remediation dashboard flow (UC-1 and UC-2).

## Files to Modify
- `src/routes.tsx` -- add route definition for `/remediation` path mapping to RemediationDashboardPage (lazy-loaded)
- `src/App.tsx` -- add navigation entry for the remediation dashboard if navigation is defined here

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` -- unit tests for the remediation dashboard page and subcomponents
- `tests/mocks/fixtures/remediation.json` -- mock remediation data (summary and by-product fixtures)
- `tests/mocks/handlers.ts` -- add MSW request handlers for GET /api/v2/remediation/summary and GET /api/v2/remediation/by-product (modify existing file if handlers.ts already exists; create if not)
- `tests/e2e/remediation-dashboard.spec.ts` -- Playwright E2E test for remediation dashboard navigation, rendering, and filtering

## Implementation Notes
- Register the route in `src/routes.tsx` using React Router v6 with a lazy-loaded import, following the pattern of existing routes (e.g., SbomListPage, AdvisoryListPage). Use `React.lazy(() => import(...))` for code splitting.
  - Applies: task modifies `src/routes.tsx` matching the convention's routing scope.
- Unit tests use Vitest + React Testing Library following the test setup in `tests/setup.ts`. Use MSW to mock API responses.
  - Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` matching the convention's testing scope.
- Create MSW handlers that return fixture data for both remediation endpoints. Follow the handler pattern in `tests/mocks/handlers.ts`:
  - `rest.get('/api/v2/remediation/summary', ...)` -- returns mock RemediationSummary
  - `rest.get('/api/v2/remediation/by-product', ...)` -- returns mock PaginatedProductRemediation
- Fixture data in `tests/mocks/fixtures/remediation.json` should include:
  - A summary with non-zero counts across all severity levels and statuses
  - A by-product response with at least 3 products for filter testing
- E2E test in `tests/e2e/remediation-dashboard.spec.ts` follows the Playwright pattern from `tests/e2e/sbom-list.spec.ts`:
  - Navigate to /remediation
  - Verify summary cards render with expected counts
  - Verify progress chart is visible
  - Verify vulnerability table renders with data
  - Apply a severity filter and verify table updates
  - Apply a product filter and verify dashboard updates
- Use PascalCase for component files, camelCase for test utility files, kebab-case for fixture file names.
  - Applies: task creates `tests/mocks/fixtures/remediation.json` matching the convention's naming scope.

## Reuse Candidates
- `tests/setup.ts` -- test setup with MSW handlers and render helpers; reuse for test configuration
- `tests/mocks/handlers.ts` -- existing MSW handler file; extend with remediation handlers
- `tests/mocks/fixtures/sboms.json` -- reference for fixture data structure
- `tests/e2e/sbom-list.spec.ts` -- reference for Playwright E2E test structure and navigation patterns
- `src/pages/SbomListPage/SbomListPage.test.tsx` -- reference for page-level unit test structure with RTL

## Acceptance Criteria
- [ ] /remediation route is registered and navigable in the application
- [ ] RemediationDashboardPage is lazy-loaded (code-split)
- [ ] MSW handlers intercept both remediation API endpoints in tests
- [ ] Fixture data covers all severity levels and multiple products
- [ ] Unit tests verify summary cards, progress chart, and vulnerability table rendering
- [ ] Unit tests verify filter interactions update displayed data
- [ ] E2E test covers navigation to /remediation, data rendering, and filter operations
- [ ] All tests pass: `npm test` (unit) and `npx playwright test` (E2E)

## Test Requirements
- [ ] Unit test: dashboard page renders summary cards with correct totals
- [ ] Unit test: loading spinner appears while API calls are in-flight
- [ ] Unit test: empty state renders when API returns no data
- [ ] Unit test: applying severity filter updates vulnerability table
- [ ] Unit test: applying product filter updates summary cards and table
- [ ] E2E test: navigate to /remediation, verify cards and chart render
- [ ] E2E test: apply product filter, verify dashboard updates to show filtered data

## Verification Commands
- `npm test -- --run RemediationDashboardPage` -- unit tests pass
- `npx playwright test remediation-dashboard` -- E2E test passes

## Dependencies
- Depends on: Task 6 -- Add filterable vulnerability table to remediation dashboard

---
Description digest: sha256-md:6e781ebc278c6828d8324595d93226cfc8369568e3f51340dbf785034c29756b

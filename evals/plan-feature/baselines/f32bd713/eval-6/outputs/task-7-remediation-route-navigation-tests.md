## Repository
trustify-ui

## Parent Epic
TC-9008 (TC-9006: trustify-ui)

## Target Branch
main

## Description
Register the `/remediation` route in the application router, add a navigation entry for the remediation dashboard, and create unit/component tests with MSW mock handlers for the complete remediation dashboard. This task wires the dashboard into the application's navigation and ensures test coverage for all remediation page components.

## Files to Modify
- `src/routes.tsx` -- add `/remediation` route definition with lazy-loaded RemediationDashboardPage component
- `src/App.tsx` -- add navigation entry/link for the remediation dashboard in the application navigation structure
- `tests/mocks/handlers.ts` -- add MSW request handlers for `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` -- component tests for the full remediation dashboard page
- `tests/mocks/fixtures/remediation.json` -- mock remediation data fixture for MSW handlers

## Implementation Notes
- Add the route definition in `src/routes.tsx` using `React.lazy()` for code splitting, following the existing pattern for other page routes.
  Per CONVENTIONS.md section Routing: React Router v6 with lazy-loaded page components.
  Applies: task modifies `src/routes.tsx` matching the convention's TypeScript routing scope.
- The navigation entry should be added in the appropriate section of the app's navigation structure (sidebar or header nav, depending on existing patterns in `src/App.tsx`).
- Create comprehensive MSW handlers in `tests/mocks/handlers.ts` that return fixture data for both remediation endpoints, enabling component tests to run without a real backend.
  Per CONVENTIONS.md section Testing: Vitest + React Testing Library for unit tests; Playwright for E2E; MSW for API mocking.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` matching the convention's TypeScript test scope.
- The `remediation.json` fixture should include a representative dataset: multiple severity/status combinations for summary, multiple products for by-product breakdown.
- Component tests should verify:
  - Page renders at the `/remediation` route
  - Summary cards display correct data from mock response
  - Filter interactions update the table
  - Loading and error states are handled

## Reuse Candidates
- `src/routes.tsx` -- existing route definitions to follow for pattern consistency
- `tests/setup.ts` -- test setup configuration with MSW server and render helpers
- `tests/mocks/handlers.ts` -- existing MSW request handler patterns for API endpoints
- `tests/mocks/fixtures/sboms.json` -- mock data fixture format reference
- `tests/mocks/fixtures/advisories.json` -- mock data fixture format reference
- `src/pages/SbomListPage/SbomListPage.test.tsx` -- page component test pattern with MSW

## Acceptance Criteria
- [ ] Route `/remediation` is registered in `src/routes.tsx` and renders RemediationDashboardPage
- [ ] Navigation entry for the remediation dashboard is visible in the application navigation
- [ ] Lazy loading works correctly for the RemediationDashboardPage component
- [ ] MSW handlers return mock data for both remediation API endpoints
- [ ] Component tests pass for the RemediationDashboardPage
- [ ] Mock fixture data covers multiple severity/status combinations and multiple products

## Test Requirements
- [ ] Test that navigating to `/remediation` renders the RemediationDashboardPage component
- [ ] Test that the navigation link for remediation dashboard is present and functional
- [ ] Test that the dashboard renders summary cards with correct data from MSW mock
- [ ] Test that the vulnerability table renders with mock data
- [ ] Test filter interactions update the displayed data
- [ ] Test loading state shows spinner while data is being fetched
- [ ] Test error state is handled when API returns an error response

## Dependencies
- Depends on: Task 5 -- Add RemediationDashboardPage with summary cards and progress chart
- Depends on: Task 6 -- Add filterable vulnerability table to remediation dashboard

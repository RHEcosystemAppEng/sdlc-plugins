## Repository
trustify-ui

## Target Branch
main

## Description
Add unit tests (Vitest + React Testing Library), MSW mock handlers, mock fixture data, and a Playwright E2E test for the remediation dashboard page. This ensures the dashboard renders correctly, filters work, and the page is navigable end-to-end.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — unit tests for dashboard rendering, summary cards, and vulnerability table
- `tests/mocks/fixtures/remediation.json` — mock remediation data for summary and by-product responses
- `tests/e2e/remediation-dashboard.spec.ts` — Playwright E2E test for dashboard navigation and interaction

## Files to Modify
- `tests/mocks/handlers.ts` — add MSW request handlers for `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`

## Implementation Notes
- Follow the testing pattern established in existing page tests like `src/pages/SbomListPage/SbomListPage.test.tsx` and `src/pages/AdvisoryListPage/AdvisoryListPage.test.tsx` — use Vitest + React Testing Library with MSW for API mocking.
  Per CONVENTIONS.md: Vitest + React Testing Library for unit tests; Playwright for E2E; MSW for API mocking.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` matching the convention's .test.tsx test file scope.
- Use the test setup from `tests/setup.ts` which configures MSW handlers and render helpers.
- Add MSW handlers in `tests/mocks/handlers.ts` following the existing pattern — handlers for both remediation endpoints returning data from `tests/mocks/fixtures/remediation.json`.
- Mock fixture data should include realistic remediation data covering all severity levels and multiple products to exercise rendering and filtering paths.
- E2E test in `tests/e2e/remediation-dashboard.spec.ts` should follow the pattern in `tests/e2e/sbom-list.spec.ts` — navigate to `/remediation`, verify page loads, interact with filters, and verify table content.
- Unit tests should cover: dashboard renders summary cards with correct counts, empty state renders when no data, vulnerability table renders rows, filter interactions update displayed rows.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.test.tsx` — reference for page-level unit test patterns
- `tests/setup.ts` — test setup with MSW handlers and render helpers
- `tests/mocks/handlers.ts` — existing MSW handler patterns to follow
- `tests/mocks/fixtures/sboms.json` — reference for mock fixture data structure
- `tests/e2e/sbom-list.spec.ts` — reference for Playwright E2E test pattern

## Acceptance Criteria
- [ ] Unit tests verify summary cards render with correct Open, In Progress, and Resolved counts
- [ ] Unit tests verify empty state renders when API returns no data
- [ ] Unit tests verify vulnerability table renders rows from mock data
- [ ] Unit tests verify filter interactions update the displayed table rows
- [ ] MSW handlers correctly intercept and respond to both remediation endpoints
- [ ] E2E test navigates to `/remediation` and verifies dashboard loads with expected content

## Test Requirements
- [ ] Unit test: dashboard page renders summary cards with mock data
- [ ] Unit test: dashboard page shows empty state with no remediation data
- [ ] Unit test: vulnerability table renders correct number of rows
- [ ] Unit test: severity filter reduces visible rows to matching severity only
- [ ] Unit test: product filter reduces visible rows to matching product only
- [ ] E2E test: navigate to /remediation, verify summary cards and table are visible

## Verification Commands
- `npx vitest run src/pages/RemediationDashboardPage` — run unit tests for the dashboard page
- `npx playwright test tests/e2e/remediation-dashboard.spec.ts` — run E2E test for the dashboard

## Dependencies
- Depends on: Task 5 — Create remediation dashboard page with summary cards and progress chart
- Depends on: Task 6 — Add filterable vulnerability table to remediation dashboard

[sdlc-workflow] Description digest: sha256-md:0f5ff06cd35eb7d8da596596336f8f9c828f9d31d0ae2699601b46088c8ecebe

# Task 7: Add tests for remediation dashboard

Parent Epic: TC-9006: trustify-ui

## Repository
trustify-ui

## Target Branch
main

## Description
Add unit tests, mock data, and an E2E test for the remediation dashboard page. Unit tests verify component rendering, data display, and filter interactions using MSW for API mocking. The E2E test verifies the complete dashboard flow in a browser using Playwright.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — unit tests for the dashboard page, summary cards, and vulnerability table
- `tests/mocks/fixtures/remediation.json` — mock remediation API response data for MSW handlers
- `tests/e2e/remediation-dashboard.spec.ts` — Playwright E2E test for the remediation dashboard flow

## Files to Modify
- `tests/mocks/handlers.ts` — add MSW request handlers for `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`

## Implementation Notes
- Per CONVENTIONS.md §Testing: use Vitest + React Testing Library for unit tests, Playwright for E2E tests, and MSW for API mocking. Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` matching the convention's .tsx scope.
- Per CONVENTIONS.md §Testing: use MSW request handlers in `tests/mocks/handlers.ts` to intercept API calls. Applies: task modifies `tests/mocks/handlers.ts` matching the convention's .ts scope.
- Reference `tests/setup.ts` for test setup configuration, MSW server initialization, and render helpers.
- Reference `src/pages/SbomListPage/SbomListPage.test.tsx` for the unit test structure — how it renders the page, waits for data to load, and asserts on rendered content.
- Reference `tests/e2e/sbom-list.spec.ts` for the Playwright E2E test structure.
- Reference `tests/mocks/fixtures/sboms.json` for the mock fixture data format.
- Mock data in `remediation.json` should include multiple severity levels and products to enable meaningful assertions.
- Unit test cases: dashboard renders loading state, summary cards display correct counts, progress chart renders, vulnerability table renders with data, filter interactions update displayed data.
- E2E test cases: navigate to `/remediation`, verify summary cards are visible, interact with filters, verify table updates.
- Add MSW handlers for both remediation endpoints that return the fixture data.

## Reuse Candidates
- `tests/setup.ts` — test setup with MSW server and render helpers; reuse for test configuration
- `tests/mocks/handlers.ts` — existing MSW handlers; extend with remediation endpoint handlers
- `tests/mocks/fixtures/sboms.json` — mock fixture format; reference for structuring remediation fixture data
- `src/pages/SbomListPage/SbomListPage.test.tsx` — unit test patterns for page components; reference for rendering, waiting, and asserting
- `tests/e2e/sbom-list.spec.ts` — Playwright E2E test patterns; reference for navigation, element selection, and assertions

## Acceptance Criteria
- [ ] Unit tests render `RemediationDashboardPage` and verify summary cards display correct count values
- [ ] Unit tests verify the progress chart component renders without errors
- [ ] Unit tests verify the vulnerability table renders rows from mock data
- [ ] Unit tests verify filter interactions (selecting a severity filter updates displayed data)
- [ ] MSW handlers for both remediation endpoints return valid mock data
- [ ] Mock fixture data in `remediation.json` covers multiple severities and products
- [ ] E2E test navigates to `/remediation` and verifies dashboard elements are visible
- [ ] E2E test interacts with a filter and verifies the table updates
- [ ] All tests pass

## Test Requirements
- [ ] At least 5 unit test cases covering rendering, data display, and filter interaction
- [ ] At least 2 E2E test cases covering page load and filter interaction

## Verification Commands
- `npx vitest run RemediationDashboardPage` — unit tests pass
- `npx playwright test remediation-dashboard` — E2E test passes

## Dependencies
- Depends on: Task 6 — Add filterable vulnerability table to remediation dashboard

## Repository
trustify-ui

## Target Branch
main

## Description
Add comprehensive tests for the Remediation Dashboard page and its components. This includes unit tests using Vitest and React Testing Library, MSW mock handlers and fixture data for the remediation endpoints, and an E2E test using Playwright to verify the full user flow of navigating to the dashboard, viewing summary cards, and using filters.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — unit tests for the dashboard page, summary cards, chart, and filter interactions
- `tests/mocks/fixtures/remediation-summary.json` — mock data fixture for the remediation summary endpoint
- `tests/mocks/fixtures/remediation-by-product.json` — mock data fixture for the remediation by-product endpoint
- `tests/e2e/remediation-dashboard.spec.ts` — Playwright E2E test for the remediation dashboard flow

## Files to Modify
- `tests/mocks/handlers.ts` — add MSW request handlers for `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`

## Implementation Notes
- Follow the existing test patterns. See `src/pages/SbomListPage/SbomListPage.test.tsx` for the established unit test pattern with React Testing Library.
  Per CONVENTIONS.md §Testing: Vitest + React Testing Library for unit tests; Playwright for E2E; MSW for API mocking.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` matching the convention's `.tsx` test file scope.
- MSW handlers: add handlers in `tests/mocks/handlers.ts` following the existing pattern. See existing handlers for `GET /api/v2/sbom` and `GET /api/v2/advisory` as references.
- Fixture data should include realistic remediation data with multiple severities, statuses, and products to exercise all filter paths.
- E2E test pattern: see `tests/e2e/sbom-list.spec.ts` for the established Playwright test pattern.
- Unit tests should cover: (a) page renders with data, (b) loading state, (c) empty state, (d) filter interactions, (e) summary card values match data.
- Per docs/constraints.md §5.11: add a doc comment to every test function created.

## Reuse Candidates
- `tests/setup.ts` — test setup with MSW handlers and render helpers; use for test configuration
- `tests/mocks/handlers.ts` — existing MSW request handlers; follow the same handler definition pattern
- `tests/mocks/fixtures/sboms.json` — existing mock data fixture; follow the same fixture structure
- `tests/e2e/sbom-list.spec.ts` — existing Playwright E2E test; follow the same page navigation and assertion patterns

## Acceptance Criteria
- [ ] Unit tests verify RemediationDashboardPage renders summary cards with correct counts
- [ ] Unit tests verify loading and empty states display correctly
- [ ] Unit tests verify filter interactions on VulnerabilityTable
- [ ] MSW handlers for remediation endpoints return realistic mock data
- [ ] Fixture files contain valid JSON matching the remediation API response shapes
- [ ] E2E test navigates to `/remediation` and verifies the dashboard loads with data
- [ ] All tests pass in CI

## Test Requirements
- [ ] Unit test: dashboard page renders summary cards matching mock summary data
- [ ] Unit test: dashboard page shows loading spinner while data is loading
- [ ] Unit test: dashboard page shows empty state when mock returns empty data
- [ ] Unit test: selecting a severity filter updates the displayed table rows
- [ ] Unit test: selecting a product filter updates the displayed table rows
- [ ] E2E test: navigate to /remediation, verify summary cards are visible
- [ ] E2E test: apply a severity filter, verify table updates

## Dependencies
- Depends on: Task 5 — Create Remediation Dashboard page with summary cards and progress chart
- Depends on: Task 6 — Add filterable vulnerability table to remediation dashboard

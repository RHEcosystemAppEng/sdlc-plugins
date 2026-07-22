## Repository
trustify-ui

## Target Branch
main

## Description
Add comprehensive unit tests and end-to-end tests for the remediation dashboard. Unit tests cover individual components with mocked API data using MSW. E2E tests verify the full user workflow of navigating to the dashboard, viewing summary cards, and using filters.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — unit tests for the dashboard page and its subcomponents
- `tests/mocks/fixtures/remediation.json` — mock remediation data for tests
- `tests/e2e/remediation-dashboard.spec.ts` — Playwright E2E tests for the remediation dashboard

## Files to Modify
- `tests/mocks/handlers.ts` — add MSW request handlers for remediation API endpoints

## Implementation Notes
Follow the testing pattern from `src/pages/SbomListPage/SbomListPage.test.tsx` for unit tests using Vitest and React Testing Library. Add MSW handlers in `tests/mocks/handlers.ts` following the existing handler pattern for mocking remediation endpoints. Create mock fixture data in `tests/mocks/fixtures/remediation.json` following the structure of `tests/mocks/fixtures/sboms.json`. E2E tests follow the Playwright pattern in `tests/e2e/sbom-list.spec.ts`.

Per CONVENTIONS.md §Testing: Vitest + React Testing Library for unit tests, Playwright for E2E, MSW for API mocking.
Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` matching the convention's `.tsx` file scope.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.test.tsx` — unit test structure reference
- `tests/setup.ts` — test setup with MSW handlers and render helpers
- `tests/mocks/handlers.ts` — existing MSW handler patterns
- `tests/mocks/fixtures/sboms.json` — mock data structure reference
- `tests/e2e/sbom-list.spec.ts` — E2E test pattern reference

## Acceptance Criteria
- [ ] Unit tests cover dashboard page rendering with mock data
- [ ] Unit tests cover summary cards, progress chart, and vulnerability table components
- [ ] Unit tests cover loading and empty states
- [ ] Unit tests cover filter interactions
- [ ] E2E test navigates to /remediation and verifies dashboard content
- [ ] E2E test applies severity filter and verifies table updates
- [ ] MSW handlers correctly mock both remediation endpoints

## Test Requirements
- [ ] Unit test: dashboard renders summary cards with correct counts
- [ ] Unit test: filter toolbar filters vulnerability table results
- [ ] Unit test: empty state displayed when no data available
- [ ] E2E test: full navigation and interaction flow on remediation dashboard

## Dependencies
- Depends on: Task 8 — Integrate dashboard routing and navigation

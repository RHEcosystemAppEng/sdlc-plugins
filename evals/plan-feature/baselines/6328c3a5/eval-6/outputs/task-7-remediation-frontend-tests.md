## Repository
trustify-ui

## Target Branch
main

## Description
Add comprehensive frontend tests for the remediation dashboard. Create MSW mock handlers for the remediation API endpoints, add mock fixture data, and write unit tests for the dashboard page and its components using Vitest and React Testing Library.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — unit tests for the dashboard page component
- `tests/mocks/fixtures/remediation.json` — mock fixture data for remediation summary and by-product responses

## Files to Modify
- `tests/mocks/handlers.ts` — add MSW request handlers for `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`

## Implementation Notes
- Follow the testing pattern established in existing page tests. See `src/pages/SbomListPage/SbomListPage.test.tsx` for the reference test structure using Vitest + React Testing Library.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` matching the convention's `.tsx` file scope.
- Per Key Conventions: Vitest + React Testing Library for unit tests; MSW for API mocking.
  Applies: task modifies `tests/mocks/handlers.ts` matching the convention's `.ts` file scope.
- MSW handlers should return the fixture data from `tests/mocks/fixtures/remediation.json`. Create realistic fixture data covering:
  - Multiple severity levels (Critical, High, Medium, Low)
  - Multiple statuses (Open, In Progress, Resolved)
  - Multiple products for by-product breakdown
- Test scenarios should cover:
  - Successful data load: verify summary cards show correct counts
  - Successful data load: verify table renders vulnerability rows
  - Loading state: verify LoadingSpinner is shown
  - Empty state: verify EmptyStateCard is shown when no data
  - Filter interaction: verify filtering reduces visible rows
- Use the test setup from `tests/setup.ts` for MSW server initialization and render helpers.
- Mock fixture data should follow the same structure as `tests/mocks/fixtures/sboms.json` and `tests/mocks/fixtures/advisories.json`.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.test.tsx` — reference for page component test structure
- `tests/setup.ts` — test setup with MSW handlers and render helpers
- `tests/mocks/handlers.ts` — existing MSW handlers showing the pattern for adding new handlers
- `tests/mocks/fixtures/sboms.json` — reference for mock fixture data structure

## Acceptance Criteria
- [ ] MSW handlers intercept remediation API requests and return fixture data
- [ ] Dashboard page test verifies summary cards render correct counts
- [ ] Dashboard page test verifies progress chart renders
- [ ] Dashboard page test verifies vulnerability table renders rows
- [ ] Loading state test verifies LoadingSpinner appears during fetch
- [ ] Empty state test verifies EmptyStateCard appears when no data
- [ ] Filter test verifies severity filter interaction
- [ ] All tests pass with `npm test`

## Test Requirements
- [ ] Unit test: RemediationDashboardPage renders summary cards with correct Open/In Progress/Resolved counts from mock data
- [ ] Unit test: RemediationDashboardPage renders progress chart component
- [ ] Unit test: VulnerabilityTable renders correct number of rows from mock data
- [ ] Unit test: severity filter interaction reduces displayed rows
- [ ] Unit test: loading state shows spinner
- [ ] Unit test: empty state shows empty state card

## Verification Commands
- `npm test -- --run RemediationDashboardPage` — run remediation dashboard tests

## Dependencies
- Depends on: Task 5 — Create remediation dashboard page with summary cards and progress chart
- Depends on: Task 6 — Add filterable vulnerability table to remediation dashboard

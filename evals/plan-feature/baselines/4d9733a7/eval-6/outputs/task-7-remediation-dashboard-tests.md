## Repository
trustify-ui

## Target Branch
main

## Description
Add unit tests for the remediation dashboard page, including tests for the main dashboard component, summary cards, progress chart, and filterable vulnerability table. Tests use React Testing Library for component rendering and MSW (Mock Service Worker) for API response mocking, following the established testing patterns in the project.

## Files to Create
- `src/pages/RemediationDashboard/RemediationDashboard.test.tsx` — unit tests for the remediation dashboard page and its sub-components
- `tests/mocks/fixtures/remediation.json` — mock remediation data fixture for MSW handlers

## Files to Modify
- `tests/mocks/handlers.ts` — add MSW request handlers for `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`

## Implementation Notes
- Per repo conventions (Testing): use Vitest + React Testing Library for unit tests and MSW for API mocking. See `src/pages/SbomListPage/SbomListPage.test.tsx` for the canonical page test example.
  Applies: task creates `src/pages/RemediationDashboard/RemediationDashboard.test.tsx` matching the convention's TypeScript test file scope.
- Per repo conventions (Testing): use the test setup from `tests/setup.ts` which configures MSW handlers and render helpers.
  Applies: task modifies `tests/mocks/handlers.ts` matching the convention's TypeScript mock file scope.
- Mock data fixtures should include a representative dataset: multiple severity levels, multiple products, mixed remediation statuses. Follow the structure of existing fixtures in `tests/mocks/fixtures/sboms.json` and `tests/mocks/fixtures/advisories.json`.
- Test scenarios should cover: successful data loading, empty state, loading state, filter interactions, and error state.
- Per repo conventions (Naming): use PascalCase for test files matching their component names.
  Applies: task creates `src/pages/RemediationDashboard/RemediationDashboard.test.tsx` matching the convention's TypeScript file scope.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.test.tsx` — reference for page-level component test structure with data loading and table assertions
- `src/pages/AdvisoryListPage/AdvisoryListPage.test.tsx` — reference for list page test patterns
- `tests/setup.ts` — test setup with MSW handlers and render helpers; use directly
- `tests/mocks/handlers.ts` — existing MSW handlers to follow the handler registration pattern
- `tests/mocks/fixtures/sboms.json` — reference for mock data fixture structure
- `tests/mocks/fixtures/advisories.json` — reference for mock data fixture structure

## Acceptance Criteria
- [ ] Unit tests exist for `RemediationDashboard`, `SummaryCards`, `ProgressChart`, and `VulnerabilityTable` components
- [ ] MSW handlers mock both remediation API endpoints
- [ ] Mock fixture data covers multiple severity levels, products, and statuses
- [ ] All tests pass with `npm test`
- [ ] Tests cover success, loading, empty, and error states

## Test Requirements
- [ ] Verify dashboard renders with mocked remediation data
- [ ] Verify summary cards display correct counts from mock data
- [ ] Verify vulnerability table renders rows from mock data
- [ ] Verify filter interactions update the displayed data
- [ ] Verify loading spinner appears during data fetch
- [ ] Verify empty state appears when API returns no data
- [ ] Verify error state appears when API returns an error

## Verification Commands
- `npm test -- --run RemediationDashboard` — run remediation dashboard tests
- `npm test` — confirm all tests pass

## Dependencies
- Depends on: Task 5 — Create remediation dashboard page with summary cards and progress chart
- Depends on: Task 6 — Add filterable vulnerability table to remediation dashboard

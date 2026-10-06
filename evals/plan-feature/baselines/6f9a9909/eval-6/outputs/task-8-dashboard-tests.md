## Repository
trustify-ui

## Target Branch
main

## Description
Add comprehensive tests for the remediation dashboard page including unit tests with React Testing Library and MSW mock handlers for the remediation API endpoints. Cover the summary cards, progress chart, filterable vulnerability table, and page-level integration scenarios. Add mock fixtures for remediation data to the shared test fixtures directory.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` -- component tests for the remediation dashboard page and its sub-components
- `tests/mocks/fixtures/remediation.json` -- mock remediation data fixture for MSW handlers

## Files to Modify
- `tests/mocks/handlers.ts` -- add MSW request handlers for `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`

## Implementation Notes
Per CONVENTIONS.md "Testing": use Vitest + React Testing Library for unit tests and MSW for API mocking. Follow the test patterns established in existing page tests. See `src/pages/SbomListPage/SbomListPage.test.tsx` for reference.
Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` matching the convention's `.test.tsx` test file scope.

Per CONVENTIONS.md "Naming": use camelCase for test utility functions, PascalCase for component references in tests.
Applies: convention has no file-type restriction (broadly applicable).

MSW handlers should intercept the remediation API endpoints and return the mock fixture data. Follow the handler patterns in `tests/mocks/handlers.ts` for existing endpoints (sboms, advisories).

Test setup should use the helpers from `tests/setup.ts` for render utilities and MSW server configuration.

Relevant constraints from `docs/constraints.md`:
- Per SS5.4: Reuse existing test infrastructure (MSW setup, render helpers, fixture patterns).

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.test.tsx` -- reference implementation for page component test structure
- `src/pages/AdvisoryListPage/AdvisoryListPage.test.tsx` -- reference implementation for list page testing
- `tests/setup.ts` -- test setup with MSW handlers and render helpers
- `tests/mocks/handlers.ts` -- existing MSW handler patterns to follow
- `tests/mocks/fixtures/sboms.json` -- reference fixture format for mock data

## Acceptance Criteria
- [ ] MSW handlers intercept remediation summary and by-product API calls and return mock data
- [ ] Test verifies summary cards render correct Open, In Progress, and Resolved counts from mock data
- [ ] Test verifies loading state renders LoadingSpinner
- [ ] Test verifies empty state renders EmptyStateCard when API returns empty data
- [ ] Test verifies VulnerabilityTable renders rows from mock data
- [ ] Test verifies severity filter updates displayed rows
- [ ] Test verifies product filter updates displayed rows
- [ ] Mock fixture file contains representative remediation data with multiple severities, statuses, and products

## Test Requirements
- [ ] Component test: RemediationDashboardPage renders summary cards with mock data values
- [ ] Component test: RemediationDashboardPage renders loading spinner during fetch
- [ ] Component test: RemediationDashboardPage renders empty state for no data
- [ ] Component test: VulnerabilityTable renders correct number of rows from mock data
- [ ] Component test: severity filter interaction updates visible rows
- [ ] Component test: product filter interaction updates visible rows
- [ ] Integration test: full page render with MSW handlers returns expected UI state

## Dependencies
- Depends on: Task 6 -- Add remediation dashboard page with summary cards and progress chart
- Depends on: Task 7 -- Add filterable vulnerability table to remediation dashboard

## Parent Epic
TC-9008

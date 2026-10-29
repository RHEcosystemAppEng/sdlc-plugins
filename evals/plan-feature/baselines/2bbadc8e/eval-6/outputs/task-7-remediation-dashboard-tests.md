## Repository
trustify-ui

## Target Branch
main

## Description
Add comprehensive tests for the remediation dashboard page, including unit tests with React Testing Library, MSW mock handlers for remediation API endpoints, and test fixture data. This ensures the dashboard components render correctly, handle loading and error states, and filters function as expected.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — unit tests for the remediation dashboard page and its subcomponents
- `tests/mocks/fixtures/remediation.json` — mock remediation data fixture for consistent test data

## Files to Modify
- `tests/mocks/handlers.ts` — add MSW request handlers for GET /api/v2/remediation/summary and GET /api/v2/remediation/by-product

## Implementation Notes
Per CONVENTIONS.md §Testing: use Vitest + React Testing Library for unit tests and MSW for API mocking. Follow the patterns in `src/pages/SbomListPage/SbomListPage.test.tsx` for page component test structure.
Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` matching the convention's `.tsx` test file scope.

Per CONVENTIONS.md §Testing: MSW request handlers go in `tests/mocks/handlers.ts` and fixtures go in `tests/mocks/fixtures/`. Follow the existing patterns in `tests/mocks/handlers.ts` and `tests/mocks/fixtures/sboms.json`.
Applies: task modifies `tests/mocks/handlers.ts` matching the convention's `.ts` mock handler scope.

The test fixture in `remediation.json` should include:
- A summary response with non-zero counts across multiple severity levels and statuses
- A by-product response with multiple products and varying remediation counts
- Edge cases: empty results, single product, all-resolved state

Test scenarios should cover:
1. Dashboard renders summary cards with correct counts
2. Progress chart renders with trend data
3. Filter controls update the vulnerability table
4. Loading state renders spinner
5. Empty state renders empty card
6. Error state handles API failures gracefully

Use the test setup from `tests/setup.ts` for render helpers and MSW initialization.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.test.tsx` — reference for page component test structure with React Testing Library
- `tests/setup.ts` — test setup with MSW handlers and render helpers
- `tests/mocks/handlers.ts` — existing MSW handlers to follow the pattern for new remediation handlers
- `tests/mocks/fixtures/sboms.json` — reference for fixture data format
- `tests/mocks/fixtures/advisories.json` — reference for advisory-related fixture data

## Acceptance Criteria
- [ ] MSW handlers intercept GET /api/v2/remediation/summary and return fixture data
- [ ] MSW handlers intercept GET /api/v2/remediation/by-product and return fixture data
- [ ] Unit tests verify summary cards render with correct counts from fixture data
- [ ] Unit tests verify progress chart renders
- [ ] Unit tests verify filter controls update the vulnerability table
- [ ] Unit tests verify loading state shows spinner
- [ ] Unit tests verify empty state shows empty card
- [ ] All tests pass with vitest

## Test Requirements
- [ ] Test RemediationDashboardPage renders summary cards with mocked summary data
- [ ] Test RemediationDashboardPage renders progress chart
- [ ] Test VulnerabilityTable renders rows from mocked by-product data
- [ ] Test severity filter interaction updates displayed rows
- [ ] Test product filter interaction updates displayed rows
- [ ] Test loading spinner appears before data resolves
- [ ] Test empty state appears when API returns empty results
- [ ] Test error handling when API returns error status

## Dependencies
- Depends on: Task 5 — Add remediation dashboard page with summary cards and progress chart
- Depends on: Task 6 — Add filterable vulnerability table to remediation dashboard

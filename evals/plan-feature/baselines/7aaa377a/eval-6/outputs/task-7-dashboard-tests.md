## Repository
trustify-ui

## Target Branch
main

## Description
Add comprehensive unit tests and an E2E test for the remediation dashboard page. Unit tests cover component rendering, data loading states, filter behavior, and chart display using Vitest, React Testing Library, and MSW. The E2E test covers the full user workflow from navigating to the dashboard through applying filters using Playwright.

## Files to Create
- `src/pages/RemediationPage/RemediationPage.test.tsx` -- unit tests for RemediationPage and its sub-components
- `tests/mocks/fixtures/remediation.json` -- mock remediation data for MSW handlers
- `tests/e2e/remediation.spec.ts` -- Playwright E2E test for remediation dashboard workflow

## Files to Modify
- `tests/mocks/handlers.ts` -- add MSW request handlers for GET /api/v2/remediation/summary and GET /api/v2/remediation/by-product

## Implementation Notes
- Per CONVENTIONS.md (Key Conventions -- Testing): use Vitest + React Testing Library for unit tests, Playwright for E2E, and MSW for API mocking.
  Applies: task creates `src/pages/RemediationPage/RemediationPage.test.tsx` matching the convention's `.tsx` file scope.
- Follow the existing test patterns in `src/pages/SbomListPage/SbomListPage.test.tsx` and `src/pages/AdvisoryListPage/AdvisoryListPage.test.tsx` for test setup, rendering, and assertion patterns.
- Follow the MSW handler pattern in `tests/mocks/handlers.ts` for adding remediation API mock handlers.
- Follow the mock fixture format in `tests/mocks/fixtures/sboms.json` and `tests/mocks/fixtures/advisories.json` for the remediation fixture data.
- Follow the E2E test pattern in `tests/e2e/sbom-list.spec.ts` for Playwright test structure.
- E2E test should cover UC-1 (view remediation summary) and UC-2 (filter by product) user workflows.

## Reuse Candidates
- `tests/setup.ts` -- test setup with MSW handlers and render helpers; use for unit test configuration
- `tests/mocks/handlers.ts` -- existing MSW request handlers; extend with remediation endpoint handlers
- `tests/mocks/fixtures/sboms.json` -- reference mock data format; follow the same structure for remediation fixtures
- `tests/mocks/fixtures/advisories.json` -- reference mock data format; follow the same JSON structure
- `tests/e2e/sbom-list.spec.ts` -- reference Playwright E2E test; follow the same test structure and navigation patterns
- `src/pages/SbomListPage/SbomListPage.test.tsx` -- reference unit test; follow the same rendering and assertion patterns

## Acceptance Criteria
- [ ] Unit tests cover RemediationPage rendering with summary cards, chart, and table
- [ ] Unit tests cover loading and empty states
- [ ] Unit tests cover filter interactions on VulnerabilityTable
- [ ] MSW handlers correctly mock both remediation API endpoints
- [ ] E2E test verifies the full dashboard workflow (navigate, view summary, apply filters)
- [ ] All tests pass

## Test Requirements
- [ ] Unit test: RemediationPage renders summary cards with mocked data
- [ ] Unit test: RemediationPage shows loading spinner during data fetch
- [ ] Unit test: RemediationPage shows empty state when no data returned
- [ ] Unit test: VulnerabilityTable filters by severity correctly
- [ ] Unit test: VulnerabilityTable filters by product correctly
- [ ] E2E test: user navigates to /remediation and sees summary cards
- [ ] E2E test: user applies a severity filter and table updates

## Verification Commands
- `npx vitest run src/pages/RemediationPage/` -- unit tests pass
- `npx playwright test tests/e2e/remediation.spec.ts` -- E2E test passes

## Dependencies
- Depends on: Task 5 -- Create remediation dashboard page with summary cards and progress chart
- Depends on: Task 6 -- Add filterable vulnerability table to remediation dashboard

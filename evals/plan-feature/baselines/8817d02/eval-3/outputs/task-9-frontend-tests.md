# Task 9 — Add tests and MSW mocks for SBOM comparison page

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add unit tests for the SBOM comparison page components and set up MSW (Mock Service Worker) handlers and fixtures for the comparison endpoint. This provides test coverage for the comparison UI, including rendering of diff sections, toolbar interactions, empty/loading states, and URL parameter handling.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page using Vitest + React Testing Library
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison response data with representative diff data across all six categories

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW request handler for `GET /api/v2/sbom/compare` returning mock comparison data

## Implementation Notes
- Follow the existing test pattern from `src/pages/SbomListPage/SbomListPage.test.tsx` and `src/pages/SbomDetailPage/SbomDetailPage.test.tsx`:
  - Use Vitest as the test runner with React Testing Library for component rendering
  - Use MSW for API mocking (handlers registered in `tests/setup.ts`)
  - Use `render` helpers from `tests/setup.ts`
- The mock fixture in `tests/mocks/fixtures/sbom-comparison.json` should contain:
  - At least 2 added packages, 2 removed packages
  - At least 1 version change (upgrade) and 1 version change (downgrade)
  - At least 1 new vulnerability with "critical" severity and 1 with "medium"
  - At least 1 resolved vulnerability
  - At least 1 license change
- MSW handler pattern: intercept `GET */api/v2/sbom/compare*` and return the fixture data.
- Test the following scenarios:
  - Page renders empty state when no query params
  - SBOM selectors populated with data from useSboms hook
  - Diff sections render correct counts and data after comparison
  - Critical vulnerability row has highlighted styling
  - URL parameters trigger auto-comparison on page load
- Follow the existing mock fixtures pattern from `tests/mocks/fixtures/sboms.json` for data structure.
- Per docs/constraints.md §5.11: Add a doc comment to every test function.
- Per docs/constraints.md §5.12: Add given-when-then inline comments to non-trivial test functions.

## Reuse Candidates
- `tests/setup.ts` — Reuse render helpers and MSW server setup
- `tests/mocks/handlers.ts` — Follow the existing handler pattern for adding new mock endpoints
- `tests/mocks/fixtures/sboms.json` — Reference for mock data structure conventions
- `tests/mocks/fixtures/advisories.json` — Reference for advisory-related mock data
- `src/pages/SbomListPage/SbomListPage.test.tsx` — Follow the same test structure and assertion patterns

## Acceptance Criteria
- [ ] MSW handler intercepts comparison API calls and returns mock data
- [ ] Mock fixture contains representative data for all six diff categories
- [ ] Unit tests cover empty state, loading state, and loaded state with diff data
- [ ] Unit tests verify toolbar interactions (selector, compare button disabled/enabled)
- [ ] Unit tests verify critical vulnerability row highlighting
- [ ] All tests pass with `npm test` or `npx vitest`

## Test Requirements
- [ ] Test: empty state renders when page loads without query params
- [ ] Test: SBOM selectors show SBOM options from the useSboms hook
- [ ] Test: Compare button disabled when fewer than two SBOMs selected
- [ ] Test: diff sections render correct row counts matching mock data
- [ ] Test: critical severity rows in New Vulnerabilities have highlighted background
- [ ] Test: page auto-triggers comparison when loaded with left and right URL params

## Verification Commands
- `npx vitest run src/pages/SbomComparePage` — Run comparison page tests

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 8 — Implement SBOM comparison page with diff sections

sha256-md:0dc0429ca6a8a7389acd288c1a0449d3156d3061b1d56089e1c2319017545a44

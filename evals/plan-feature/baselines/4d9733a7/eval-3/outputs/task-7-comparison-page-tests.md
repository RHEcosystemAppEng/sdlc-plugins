## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add comprehensive test coverage for the SBOM comparison page including MSW request handlers for the comparison endpoint, mock fixture data, and React Testing Library component tests. This task creates the test infrastructure and verifies all comparison page behaviors including the export functionality.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` -- Component tests for the full comparison page
- `tests/mocks/fixtures/comparison.json` -- Mock SBOM comparison response data with representative entries in all six diff categories

## Files to Modify
- `tests/mocks/handlers.ts` -- Add MSW request handler for GET /api/v2/sbom/compare endpoint

## Implementation Notes
- Follow the test pattern in `src/pages/SbomDetailPage/SbomDetailPage.test.tsx` for page-level component tests.
- Add an MSW handler in `tests/mocks/handlers.ts` for `GET /api/v2/sbom/compare` that returns the mock comparison fixture data. Follow the existing handler patterns for SBOM and advisory endpoints.
- Create fixture data in `tests/mocks/fixtures/comparison.json` with representative entries:
  - 2-3 added packages (at least one with advisories)
  - 2-3 removed packages
  - 2-3 version changes (include both upgrade and downgrade)
  - 2-3 new vulnerabilities (include one with Critical severity)
  - 1-2 resolved vulnerabilities
  - 1-2 license changes
- Use React Testing Library's `render`, `screen`, and `userEvent` utilities for component tests.
- Per CONVENTIONS.md: use Vitest + React Testing Library for unit tests and MSW for API mocking.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's TypeScript test scope.
- Per CONVENTIONS.md: use kebab-case for directory names.
  Applies: task modifies `tests/mocks/handlers.ts` matching the convention's TypeScript test infrastructure scope.

## Reuse Candidates
- `src/pages/SbomDetailPage/SbomDetailPage.test.tsx` -- existing page test; follow the same render + assert pattern
- `src/pages/SbomListPage/SbomListPage.test.tsx` -- existing list page test; reference for testing tables and list components
- `tests/mocks/handlers.ts` -- existing MSW handlers; follow the same handler registration pattern
- `tests/mocks/fixtures/sboms.json` -- existing mock SBOM data; reference for fixture structure
- `tests/setup.ts` -- test setup with MSW and render helpers; use the configured test environment

## Acceptance Criteria
- [ ] MSW handler for GET /api/v2/sbom/compare returns mock comparison data
- [ ] Mock fixture includes representative data for all six diff categories
- [ ] Component tests cover empty state, loading state, and populated state
- [ ] Component tests verify that Critical severity rows are visually highlighted
- [ ] Component tests verify URL parameter reading and updating
- [ ] All tests pass with `npm run test`

## Test Requirements
- [ ] Test: page renders empty state with EmptyState component when loaded without query params
- [ ] Test: page shows loading skeletons when comparison API call is in progress
- [ ] Test: page renders all six diff sections with correct headings and counts after successful API call
- [ ] Test: Added Packages section shows correct package data from fixture
- [ ] Test: New Vulnerabilities section highlights Critical severity rows
- [ ] Test: Compare button triggers API call with selected SBOM IDs
- [ ] Test: Export dropdown is disabled before comparison and enabled after
- [ ] Test: URL query params pre-populate SBOM selectors on mount

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 5 -- Implement SBOM comparison page with diff sections
- Depends on: Task 6 -- Add export functionality for comparison results

## Repository
trustify-ui

## Target Branch
main

## Description
Add comprehensive test coverage for the SBOM comparison feature: MSW mock handler and fixture data for the comparison endpoint, unit tests for the comparison page components, and Playwright E2E tests for the full comparison workflow from SBOM list selection through comparison view.

## Files to Create
- `tests/mocks/fixtures/sbom-compare.json` — Mock SBOM comparison response data with representative entries in all six diff categories
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page component
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E test for the comparison workflow

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW request handler for `GET /api/v2/sbom/compare` returning the fixture data

## Implementation Notes
- Per CONVENTIONS.md §Testing: use Vitest + React Testing Library for unit tests, Playwright for E2E, and MSW for API mocking. See `src/pages/SbomListPage/SbomListPage.test.tsx` and `tests/e2e/sbom-list.spec.ts` for established patterns.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's `.tsx` test file scope.
- Per CONVENTIONS.md §Testing: MSW handlers are centralized in `tests/mocks/handlers.ts` with fixture data in `tests/mocks/fixtures/`. Follow the existing pattern of `sboms.json` and `advisories.json`.
  Applies: task modifies `tests/mocks/handlers.ts` matching the convention's `.ts` file scope.
- The mock comparison fixture should include:
  - At least 2 added packages (one with advisories)
  - At least 2 removed packages
  - At least 1 version change (upgrade) and 1 version change (downgrade)
  - At least 1 new vulnerability with severity "critical" (to test highlighted row)
  - At least 1 resolved vulnerability
  - At least 1 license change
- E2E test should cover the full workflow:
  1. Navigate to SBOM list page
  2. Select two SBOMs via checkboxes
  3. Click "Compare selected"
  4. Verify comparison page loads with diff sections
  5. Verify URL contains left and right params
  6. Verify sections are collapsible

## Reuse Candidates
- `tests/mocks/handlers.ts` — Existing MSW handlers; follow the pattern for adding the comparison handler
- `tests/mocks/fixtures/sboms.json` — Existing SBOM fixture data format
- `tests/mocks/fixtures/advisories.json` — Existing advisory fixture data format
- `tests/setup.ts` — Test setup with MSW and render helpers
- `src/pages/SbomListPage/SbomListPage.test.tsx` — Existing page test pattern to follow
- `tests/e2e/sbom-list.spec.ts` — Existing E2E test pattern to follow

## Acceptance Criteria
- [ ] MSW handler for `GET /api/v2/sbom/compare` is registered in `tests/mocks/handlers.ts`
- [ ] Mock fixture `sbom-compare.json` contains representative data for all six diff categories
- [ ] Unit tests pass for the comparison page empty state, loading state, and data display
- [ ] Unit test verifies that Critical vulnerability rows have highlighted styling
- [ ] E2E test covers the full workflow from list page selection through comparison view
- [ ] E2E test verifies URL-shareable comparison (navigating directly to a comparison URL loads the correct data)

## Test Requirements
- [ ] Unit test: SbomComparePage renders empty state when no query params are present
- [ ] Unit test: SbomComparePage renders loading skeleton when comparison is in progress
- [ ] Unit test: SbomComparePage renders all six diff sections with correct data from the mock
- [ ] Unit test: diff section count badges show correct counts
- [ ] Unit test: sections with 0 items are collapsed, sections with >0 items are expanded
- [ ] E2E test: select two SBOMs on list page, click Compare, verify comparison page renders
- [ ] E2E test: navigate directly to `/sbom/compare?left={id1}&right={id2}` and verify data loads

## Dependencies
- Depends on: Task 4 — Add SBOM comparison page
- Depends on: Task 5 — Add SBOM selection to list page

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add comprehensive tests for the SBOM comparison feature: MSW request handlers and fixture data for the comparison endpoint, unit tests for the comparison page component, and Playwright E2E tests that exercise the full comparison workflow from SBOM selection through diff rendering.

## Files to Modify
- `tests/mocks/handlers.ts` -- add MSW handler for GET /api/v2/sbom/compare that intercepts the comparison request and returns fixture data

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` -- unit tests for the comparison page: empty state, loading state, diff section rendering, critical vulnerability highlighting, URL parameter handling
- `tests/mocks/fixtures/sbom-comparison.json` -- mock comparison response fixture with representative data across all six diff categories
- `tests/e2e/sbom-compare.spec.ts` -- Playwright E2E test: navigate to SBOM list, select two SBOMs, click "Compare selected", verify comparison view renders with diff sections

## Implementation Notes
- Follow the existing test patterns from `src/pages/SbomListPage/SbomListPage.test.tsx` and `src/pages/SbomDetailPage/SbomDetailPage.test.tsx` for component testing with React Testing Library.
- Follow the existing MSW handler pattern in `tests/mocks/handlers.ts` for intercepting API requests. The handler should match `GET /api/v2/sbom/compare` and return the fixture from `tests/mocks/fixtures/sbom-comparison.json`.
- The fixture file should contain realistic mock data with at least:
  - 2-3 added packages (including one with advisories)
  - 1-2 removed packages
  - 2 version changes (one upgrade, one downgrade)
  - 2 new vulnerabilities (including one Critical severity for highlight testing)
  - 1 resolved vulnerability
  - 1 license change
- For E2E tests, follow the Playwright pattern from `tests/e2e/sbom-list.spec.ts`. The E2E flow should:
  1. Navigate to the SBOM list page
  2. Select two SBOMs via checkboxes
  3. Click "Compare selected"
  4. Verify the comparison page loads with the correct URL parameters
  5. Verify diff sections are rendered with data
- Use the test setup from `tests/setup.ts` for render helpers and MSW configuration.
- Test URL-shareable comparison: navigate directly to `/sbom/compare?left=id1&right=id2` and verify the comparison loads correctly without going through the list page selection flow.

## Reuse Candidates
- `tests/mocks/handlers.ts` -- existing MSW handlers; follow the handler definition pattern
- `tests/mocks/fixtures/sboms.json` -- existing SBOM fixture; reference for fixture data structure and naming
- `tests/mocks/fixtures/advisories.json` -- existing advisory fixture; reference for advisory data shape
- `tests/setup.ts` -- test setup with MSW handlers and render helpers
- `tests/e2e/sbom-list.spec.ts` -- existing Playwright E2E test; follow its structure and patterns
- `src/pages/SbomListPage/SbomListPage.test.tsx` -- existing unit test; follow testing patterns

## Acceptance Criteria
- [ ] MSW handler intercepts GET /api/v2/sbom/compare and returns mock fixture data
- [ ] Fixture file contains representative data for all six diff categories
- [ ] Unit tests cover empty state rendering
- [ ] Unit tests cover loading state (Skeleton placeholders)
- [ ] Unit tests cover diff section rendering with correct data
- [ ] Unit tests cover Critical severity highlighting in New Vulnerabilities
- [ ] Unit tests cover URL parameter reading and pre-population
- [ ] E2E test verifies the full comparison workflow from list page to comparison view
- [ ] E2E test verifies direct URL navigation to a comparison

## Test Requirements
- [ ] Unit test: comparison page shows empty state when no query params
- [ ] Unit test: comparison page shows loading skeletons during API call
- [ ] Unit test: comparison page renders Added Packages section with correct count and data
- [ ] Unit test: comparison page renders Removed Packages section with correct count and data
- [ ] Unit test: comparison page renders Version Changes section with upgrade/downgrade indicators
- [ ] Unit test: comparison page renders New Vulnerabilities with SeverityBadge and Critical highlighting
- [ ] Unit test: comparison page renders Resolved Vulnerabilities section
- [ ] Unit test: comparison page renders License Changes section
- [ ] Unit test: direct navigation to /sbom/compare?left=id1&right=id2 loads comparison
- [ ] E2E test: select 2 SBOMs on list page, click Compare, verify comparison renders
- [ ] E2E test: share URL navigation loads correct comparison

## Verification Commands
- `npx vitest run src/pages/SbomComparePage/SbomComparePage.test.tsx` -- run comparison page unit tests, expect all to pass
- `npx playwright test tests/e2e/sbom-compare.spec.ts` -- run comparison E2E tests, expect all to pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 5 -- Frontend: Build SBOM comparison page with diff sections
- Depends on: Task 6 -- Frontend: Add comparison route and SBOM list page selection

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add comprehensive unit tests and E2E tests for the SBOM comparison page. Unit tests use MSW mocks and React Testing Library. E2E tests use Playwright to verify the full user flow from SBOM selection through comparison rendering and URL sharing.

## Files to Modify
- `tests/mocks/handlers.ts` — add MSW handler for GET /api/v2/sbom/compare

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for the comparison page
- `tests/mocks/fixtures/sbom-comparison.json` — mock comparison response data
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E tests for comparison flow

## Implementation Notes
**MSW Mock Handler** (`tests/mocks/handlers.ts`):
Add a handler for `GET /api/v2/sbom/compare` that returns mock comparison data from `tests/mocks/fixtures/sbom-comparison.json`. Follow the existing handler patterns in this file for SBOM and advisory endpoints.

**Mock Fixture** (`tests/mocks/fixtures/sbom-comparison.json`):
Create a fixture matching the SbomComparisonResult shape with sample data in all six categories. Include at least one Critical severity vulnerability to test row highlighting. Reference existing fixtures in `tests/mocks/fixtures/sboms.json` for the data format pattern.

**Unit Tests** (`SbomComparePage.test.tsx`):
Follow the testing patterns from `src/pages/SbomListPage/SbomListPage.test.tsx` and `src/pages/SbomDetailPage/SbomDetailPage.test.tsx`. Use Vitest + React Testing Library with the test setup from `tests/setup.ts`.

Test scenarios:
- Renders empty state when no query params
- Populates selectors with SBOM list
- Compare button disabled state
- Renders diff sections after comparison
- Critical vulnerability row highlighting
- Export dropdown disabled until loaded
- URL params are read on mount

**E2E Tests** (`tests/e2e/sbom-compare.spec.ts`):
Follow the pattern from `tests/e2e/sbom-list.spec.ts`. Test the full flow:
- Navigate to /sbom/compare
- Select two SBOMs
- Click Compare
- Verify all diff sections are rendered
- Verify URL updates with selected SBOM IDs
- Navigate directly via URL with query params and verify comparison loads

## Reuse Candidates
- `tests/setup.ts` — test setup with MSW handlers and render helpers
- `tests/mocks/handlers.ts` — existing MSW handler patterns
- `tests/mocks/fixtures/sboms.json` — mock SBOM data format reference
- `src/pages/SbomListPage/SbomListPage.test.tsx` — unit test pattern for page components
- `tests/e2e/sbom-list.spec.ts` — E2E test pattern with Playwright

## Acceptance Criteria
- [ ] MSW handler for comparison endpoint returns valid mock data
- [ ] Mock fixture contains sample data for all six diff categories
- [ ] Unit tests cover empty state, selector interaction, comparison rendering, and export state
- [ ] E2E tests cover the full comparison workflow
- [ ] All tests pass

## Test Requirements
- [ ] Unit test: empty state renders when no query params are present
- [ ] Unit test: SBOM selectors populate correctly
- [ ] Unit test: compare button disabled/enabled state transitions
- [ ] Unit test: diff sections render with correct data
- [ ] Unit test: critical vulnerability row has highlight styling
- [ ] E2E test: full comparison flow from selection to result rendering
- [ ] E2E test: URL sharing loads comparison directly

## Verification Commands
- `npm test -- --run SbomComparePage` — expected: all unit tests pass
- `npx playwright test sbom-compare` — expected: all E2E tests pass

## Dependencies
- Depends on: Task 7 — Frontend comparison page

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add unit tests for the SBOM comparison page and supporting components, along with MSW mock handlers and fixture data for the comparison endpoint. Tests cover the page rendering states (empty, loading, loaded), SBOM selector interactions, diff section rendering, and URL parameter synchronization.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page component
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison response data with representative entries in all six diff categories

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW handler for `GET /api/v2/sbom/compare` returning mock comparison data

## Implementation Notes
Follow the test pattern in `src/pages/SbomListPage/SbomListPage.test.tsx` and `src/pages/SbomDetailPage/SbomDetailPage.test.tsx`.

**Mock fixture** (`tests/mocks/fixtures/sbom-comparison.json`):
Create a representative comparison response with at least 2 entries in each diff category. Include a critical-severity vulnerability in `new_vulnerabilities` to test highlighted row rendering.

**MSW handler** (`tests/mocks/handlers.ts`):
Add a handler for `GET /api/v2/sbom/compare` that returns the fixture data. Support `left` and `right` query parameters — return 400 if either is missing, return the fixture for valid requests.

**Page tests** (`SbomComparePage.test.tsx`):
- Use `render()` from React Testing Library with `MemoryRouter` for route context
- Use `QueryClientProvider` for React Query context
- Test cases:
  1. Renders `EmptyState` when no query params → verify "Select two SBOMs to compare" text
  2. Renders loading skeletons when comparison is in-flight
  3. Renders all six diff sections with correct titles and badge counts after API response
  4. SBOM selectors display options from the SBOM list endpoint
  5. Clicking "Compare" updates URL search params
  6. Critical severity rows in New Vulnerabilities have highlighted styling
  7. Pre-populates selectors from URL query params `left` and `right`

Per CONVENTIONS.md §Testing: Vitest + React Testing Library for unit tests; MSW for API mocking.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's `.test.tsx` file scope.

Per CONVENTIONS.md §Naming: PascalCase for components, camelCase for hooks and utilities.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's component naming scope.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.test.tsx` — reference for page-level test setup with React Testing Library and MSW
- `src/pages/SbomDetailPage/SbomDetailPage.test.tsx` — reference for testing pages with async data loading
- `tests/setup.ts` — test setup with MSW handlers and render helpers
- `tests/mocks/handlers.ts` — existing MSW handlers to follow as pattern
- `tests/mocks/fixtures/sboms.json` — reference for fixture data format

## Acceptance Criteria
- [ ] MSW handler for `GET /api/v2/sbom/compare` is registered in `tests/mocks/handlers.ts`
- [ ] Mock fixture contains representative data for all six diff categories
- [ ] Page test verifies empty state rendering
- [ ] Page test verifies loading state rendering
- [ ] Page test verifies all six diff sections render with correct data
- [ ] Page test verifies URL parameter pre-population
- [ ] All tests pass: `npx vitest run`

## Test Requirements
- [ ] At least 7 test cases covering empty state, loading, loaded sections, selector interaction, URL params, critical severity highlighting, and compare button behavior
- [ ] Tests use MSW for API mocking — no direct Axios mocking

## Verification Commands
- `npx vitest run --reporter=verbose -- SbomComparePage` — page tests pass
- `npx vitest run` — full test suite passes (no regressions)

## Dependencies
- Depends on: Task 1 — create-branch
- Depends on: Task 7 — frontend-comparison-page

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "Critical"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}

[sdlc-workflow] Description digest: sha256-md:93a376e0f549ad41c4aee74db2a27c86e925faf7af62d682d417b7b6d77aedbe

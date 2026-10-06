## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add comprehensive unit tests (Vitest + React Testing Library) and E2E tests (Playwright) for the SBOM comparison page, including MSW mock handlers and fixture data. This task ensures the comparison feature has full test coverage across the data layer, component rendering, user interactions, and end-to-end user workflows.

## Files to Create
- `src/pages/SbomComparisonPage/SbomComparisonPage.test.tsx` — unit tests for the comparison page component
- `tests/mocks/fixtures/sbom-comparison.json` — mock comparison API response fixture data
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E test for the comparison workflow

## Files to Modify
- `tests/mocks/handlers.ts` — add MSW request handler for `GET /api/v2/sbom/compare`

## Implementation Notes
Per the frontend testing convention: Vitest + React Testing Library for unit tests, Playwright for E2E, MSW for API mocking. Follow the existing test patterns.
Applies: task creates `src/pages/SbomComparisonPage/SbomComparisonPage.test.tsx` matching the convention's TypeScript test file scope.

Per the frontend naming convention: test files use `.test.tsx` suffix co-located with the component, E2E tests use `.spec.ts` in `tests/e2e/`.
Applies: task creates `tests/e2e/sbom-compare.spec.ts` matching the convention's E2E test scope.

**MSW handler:**
- Intercept `GET /api/v2/sbom/compare` requests
- Return fixture data from `tests/mocks/fixtures/sbom-comparison.json`
- Handle error cases (missing params → 400, not found → 404)

**Fixture data structure:**
Create a realistic comparison fixture with entries in each diff category to enable comprehensive component rendering tests:
- 2-3 added packages
- 1-2 removed packages
- 2 version changes (one upgrade, one downgrade)
- 2 new vulnerabilities (one critical, one medium — to test highlighted row)
- 1 resolved vulnerability
- 1 license change

**Unit test coverage areas:**
- Empty state rendering (no comparison active)
- Loading state rendering (skeletons)
- Full result rendering (all six sections)
- Section expand/collapse behavior (expanded when >0 items)
- Critical severity row highlighting in New Vulnerabilities
- SBOM selector interaction
- Compare button enable/disable logic
- URL query parameter reading and writing

**E2E test workflow (UC-1):**
1. Navigate to SBOM list page
2. Select two SBOMs via checkboxes
3. Click "Compare selected"
4. Verify navigation to comparison page with correct URL params
5. Verify diff sections render with expected data
6. Verify sections are expandable/collapsible

**E2E test workflow (UC-2):**
1. Navigate directly to `/sbom/compare?left={id1}&right={id2}`
2. Verify comparison auto-triggers
3. Verify results display without manual Compare click

## Reuse Candidates
- `tests/setup.ts` — existing test setup with MSW handlers and render helpers
- `tests/mocks/handlers.ts` — existing MSW request handlers to follow for handler pattern
- `tests/mocks/fixtures/sboms.json` — existing mock SBOM data fixture pattern
- `tests/e2e/sbom-list.spec.ts` — existing Playwright E2E test to follow for test structure and assertions
- `src/pages/SbomListPage/SbomListPage.test.tsx` — existing page-level unit test pattern

## Acceptance Criteria
- [ ] MSW handler intercepts comparison endpoint requests and returns fixture data
- [ ] MSW handler returns 400 for missing query parameters
- [ ] Unit tests cover all six diff sections rendering correctly
- [ ] Unit tests verify empty state and loading state rendering
- [ ] Unit tests verify Compare button enable/disable logic
- [ ] Unit tests verify critical severity row highlighting
- [ ] E2E test covers the list-page-to-comparison-page workflow (UC-1)
- [ ] E2E test covers the direct-URL comparison workflow (UC-2)
- [ ] All tests pass (`npm test` and `npx playwright test`)

## Test Requirements
- [ ] Unit test: comparison page renders empty state when no IDs are provided
- [ ] Unit test: comparison page renders loading skeletons during API call
- [ ] Unit test: comparison page renders all diff sections with fixture data
- [ ] Unit test: Added Packages section shows correct count badge and table columns
- [ ] Unit test: New Vulnerabilities section highlights critical severity rows
- [ ] Unit test: sections with 0 items are collapsed by default
- [ ] Unit test: URL params are set after clicking Compare
- [ ] E2E test: full comparison workflow from SBOM list page selection
- [ ] E2E test: direct URL navigation triggers auto-comparison

## Verification Commands
- `npm test -- --run SbomComparisonPage` — run comparison page unit tests
- `npx playwright test sbom-compare` — run comparison E2E tests

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 6 — Add comparison route and SBOM list page compare action

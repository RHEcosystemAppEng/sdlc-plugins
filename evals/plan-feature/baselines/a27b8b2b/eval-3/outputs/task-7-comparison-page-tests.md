# Task 7: Add frontend tests for SbomComparePage

**Summary**: Add unit and E2E tests for SBOM comparison page

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add comprehensive unit tests and end-to-end tests for the SBOM comparison feature. Unit tests cover the SbomComparePage component, its sub-components (diff sections, toolbar), and the useSbomComparison hook. E2E tests cover the full user workflow: navigating from the SBOM list, selecting two SBOMs, clicking Compare, and verifying the comparison results render correctly.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the SbomComparePage component and its sub-components
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison API response fixture data
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E tests for the comparison workflow

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW request handler for `GET /api/v2/sbom/compare` that returns the mock comparison fixture

## Implementation Notes
- Follow the existing test patterns:
  - Unit tests: Vitest + React Testing Library pattern from `src/pages/SbomListPage/SbomListPage.test.tsx` and `src/pages/SbomDetailPage/SbomDetailPage.test.tsx`
  - E2E tests: Playwright pattern from `tests/e2e/sbom-list.spec.ts`
  - MSW handlers: follow the handler registration pattern in `tests/mocks/handlers.ts`
  - Mock fixtures: follow the JSON fixture pattern in `tests/mocks/fixtures/sboms.json`
- The mock comparison fixture should include realistic data for all six diff categories to ensure comprehensive rendering tests.
- Unit tests should verify:
  - Component rendering in all states (empty, loading, data, error)
  - User interactions (selecting SBOMs, clicking Compare, expanding/collapsing sections)
  - Correct PatternFly component usage (Badge colors, ExpandableSection state, Table sorting)
  - Critical vulnerability row highlighting
  - URL parameter synchronization
- E2E tests should verify:
  - Full workflow: SBOM list → select two → Compare → view results
  - URL-shareable comparison: direct navigation to `/sbom/compare?left=id1&right=id2`
  - Empty state rendering on initial page load
- Use the test setup from `tests/setup.ts` for render helpers and MSW server configuration.

## Reuse Candidates
- `tests/setup.ts` — test setup with MSW handlers and render helpers
- `tests/mocks/handlers.ts` — existing MSW request handlers; follow the pattern for adding the comparison handler
- `tests/mocks/fixtures/sboms.json` — existing mock SBOM data; reference for fixture format
- `tests/mocks/fixtures/advisories.json` — existing mock advisory data; reference for fixture format
- `tests/e2e/sbom-list.spec.ts` — existing Playwright E2E tests; follow the same navigation and assertion patterns
- `src/pages/SbomListPage/SbomListPage.test.tsx` — existing unit tests for a list page; follow test structure
- `src/pages/SbomDetailPage/SbomDetailPage.test.tsx` — existing unit tests for a detail page; follow component rendering test patterns

## Acceptance Criteria
- [ ] Unit tests cover all SbomComparePage states: empty, loading, data rendered, error
- [ ] Unit tests verify correct Badge colors for each diff section
- [ ] Unit tests verify critical vulnerability row highlighting
- [ ] Unit tests verify Compare button disabled state when selectors are incomplete
- [ ] MSW handler for comparison endpoint returns realistic mock data
- [ ] E2E test covers the full workflow: list → select → compare → verify results
- [ ] E2E test covers direct URL navigation with pre-populated query params
- [ ] All tests pass (`npm run test` and `npx playwright test`)

## Test Requirements
- [ ] Unit test: SbomComparePage renders EmptyState when no comparison is loaded
- [ ] Unit test: SbomComparePage renders Skeleton loading state during API call
- [ ] Unit test: SbomComparePage renders all six diff sections with correct data
- [ ] Unit test: Added Packages section Badge is green; Removed Packages Badge is red
- [ ] Unit test: Version Changes section Badge is blue; License Changes Badge is yellow
- [ ] Unit test: New Vulnerabilities rows with "critical" severity have highlighted background
- [ ] Unit test: ExpandableSection is expanded by default for sections with items > 0
- [ ] E2E test: select two SBOMs on list page, click Compare, verify comparison page renders with results
- [ ] E2E test: navigate directly to `/sbom/compare?left=id1&right=id2`, verify comparison auto-loads

## Verification Commands
- `npm run test -- --run SbomComparePage` — runs unit tests for the comparison page; all tests should pass
- `npx playwright test sbom-compare` — runs E2E tests for the comparison workflow; all tests should pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add SbomComparePage with diff sections UI
- Depends on: Task 6 — Add comparison route and SbomListPage multi-select

## Repository
trustify-ui

## Target Branch
main

## Description
Add MSW (Mock Service Worker) request handlers for the SBOM comparison endpoint and create component tests for the comparison page and the SBOM list page selection behavior. Tests verify the full user workflow: selecting SBOMs, triggering comparisons, and viewing diff results.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — component tests for the comparison page
- `tests/mocks/fixtures/comparison.json` — mock comparison API response data

## Files to Modify
- `tests/mocks/handlers.ts` — add MSW handler for `GET /api/v2/sbom/compare`
- `src/pages/SbomListPage/SbomListPage.test.tsx` — add tests for multi-select and "Compare selected" navigation

## Implementation Notes
Follow the existing test patterns:
- `tests/mocks/handlers.ts` defines MSW request handlers — add a handler for `GET /api/v2/sbom/compare` that returns mock comparison data from `tests/mocks/fixtures/comparison.json`
- `tests/mocks/fixtures/sboms.json` contains mock SBOM data — create `comparison.json` with sample diff data covering all six sections
- `src/pages/SbomListPage/SbomListPage.test.tsx` contains existing list page tests — add tests for checkbox selection and navigation
- `tests/setup.ts` defines test setup with MSW handlers and render helpers — use the same helpers
- Use Vitest + React Testing Library for component tests
- Test the comparison page: initial empty state, loading state, rendered diff sections with correct data
- Test the list page: checkbox rendering, selection limits, navigation on button click

Per CONVENTIONS.md §Testing: Vitest + React Testing Library for unit tests; MSW for API mocking.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's test file scope.

## Reuse Candidates
- `tests/mocks/handlers.ts` — existing MSW handlers, reference for handler registration pattern
- `tests/mocks/fixtures/sboms.json` — existing mock data fixture, reference for fixture file format
- `tests/setup.ts` — test setup with render helpers, use for component test boilerplate
- `src/pages/SbomDetailPage/SbomDetailPage.test.tsx` — existing page test, reference for page component testing pattern

## Acceptance Criteria
- [ ] MSW handler for `GET /api/v2/sbom/compare` is registered and returns mock data
- [ ] Mock comparison fixture includes sample data for all six diff sections
- [ ] Comparison page component tests cover: empty state, loading state, rendered diff results
- [ ] SBOM list page tests cover: checkbox selection, "Compare selected" button state, navigation
- [ ] All tests pass with `vitest`

## Test Requirements
- [ ] Test comparison page renders empty state when no query params are present
- [ ] Test comparison page shows loading skeletons during API call
- [ ] Test comparison page renders all six diff sections with correct row counts from mock data
- [ ] Test SBOM list page checkbox selection limits to 2 items
- [ ] Test "Compare selected" navigates to correct URL with selected SBOM IDs

## Dependencies
- Depends on: Task 7 — Frontend comparison page
- Depends on: Task 8 — Frontend SBOM list compare action

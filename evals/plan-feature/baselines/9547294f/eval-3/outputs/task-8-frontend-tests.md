# Task 8 — Add tests for SBOM comparison frontend components

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add comprehensive unit tests and E2E tests for the SBOM comparison feature. Unit tests cover the comparison page component behavior (empty state, loading, diff rendering, selection interactions) using Vitest and React Testing Library with MSW mocks. E2E tests cover the full comparison workflow from SBOM list selection through diff rendering using Playwright.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page component
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison API response fixture
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E test for the comparison workflow

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW handler for GET /api/v2/sbom/compare returning the mock fixture

## Implementation Notes

### Unit test coverage

Follow the existing test patterns in `src/pages/SbomListPage/SbomListPage.test.tsx` and `src/pages/SbomDetailPage/SbomDetailPage.test.tsx`:
- Use Vitest + React Testing Library
- Use MSW for API mocking via the shared handlers in `tests/mocks/handlers.ts`
- Use the render helpers from `tests/setup.ts`

Key test scenarios:
1. Empty state renders when no query params are present
2. Loading state (Skeleton) renders while API call is in progress
3. All six diff sections render with correct data from mock response
4. Sections with zero items are collapsed by default
5. New Vulnerabilities rows with Critical severity have visual emphasis
6. Compare button is disabled until both selectors have values
7. URL updates when comparison is triggered

### Mock fixture

Create `tests/mocks/fixtures/sbom-comparison.json` with a realistic comparison result:
- 2-3 added packages, 1-2 removed packages, 2 version changes
- 1 new vulnerability (critical severity), 1 resolved vulnerability
- 1 license change

### E2E test

Follow the existing E2E pattern in `tests/e2e/sbom-list.spec.ts`:
- Navigate to SBOM list page
- Select two SBOMs via checkboxes
- Click "Compare selected"
- Verify navigation to `/sbom/compare` with correct query params
- Verify diff sections render with expected data

### Reuse candidates

- `src/pages/SbomListPage/SbomListPage.test.tsx` — existing page test pattern for reference
- `src/pages/SbomDetailPage/SbomDetailPage.test.tsx` — existing detail page test pattern
- `tests/setup.ts` — shared test setup with MSW and render helpers
- `tests/mocks/handlers.ts` — existing MSW handlers to extend
- `tests/mocks/fixtures/sboms.json` — existing mock SBOM data for the list endpoint
- `tests/e2e/sbom-list.spec.ts` — existing E2E test pattern for Playwright

Per CONVENTIONS.md: use Vitest + React Testing Library for unit tests; Playwright for E2E; MSW for API mocking.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's TypeScript test file scope.

## Acceptance Criteria
- [ ] All unit tests pass via Vitest
- [ ] E2E test passes via Playwright
- [ ] MSW handler correctly mocks the comparison endpoint
- [ ] Mock fixture contains realistic comparison data
- [ ] Test coverage includes empty state, loading state, data rendering, and user interactions

## Test Requirements
- [ ] Unit test: empty state renders with EmptyState component when no comparison is active
- [ ] Unit test: loading Skeleton renders while comparison API is in progress
- [ ] Unit test: Added Packages section renders with correct package data
- [ ] Unit test: Removed Packages section renders with correct package data
- [ ] Unit test: Version Changes section renders with left/right versions and direction
- [ ] Unit test: New Vulnerabilities section renders with SeverityBadge and Critical row highlighting
- [ ] Unit test: Resolved Vulnerabilities section renders correctly
- [ ] Unit test: License Changes section renders with left/right license values
- [ ] Unit test: Compare button disabled state with zero/one selector values
- [ ] E2E test: full comparison workflow from SBOM list selection to diff rendering

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 6 — Add SBOM comparison page with diff sections
- Depends on: Task 7 — Add SBOM selection and comparison trigger on list page

---
Priority: Critical
Fix Versions: RHTPA 1.5.0
Labels: ai-generated-jira

[sdlc-workflow] Description digest: sha256-md:b0e4a8c2d7f3916e5b1c4f6a8d0e3b5c7f9a2d4e6b8c1f3a5d7e9b0c2f4a6d8e

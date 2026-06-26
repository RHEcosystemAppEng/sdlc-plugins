## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add MSW mock handlers for the comparison endpoint and Playwright E2E tests that verify the full comparison workflow: selecting two SBOMs from the list page, navigating to the comparison view, and seeing the structured diff results.

## Files to Create
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison response fixture with representative data across all six diff categories
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E tests for the comparison workflow

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW handler for `GET /api/v2/sbom/compare` that returns the mock fixture
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Add unit tests for the comparison page (create file if it doesn't exist alongside the page component)

## Implementation Notes
**MSW Handler** in `tests/mocks/handlers.ts`:
Follow the existing handler patterns for SBOM and advisory endpoints. Add a handler for `GET /api/v2/sbom/compare` that:
- Reads `left` and `right` query params
- Returns the fixture from `tests/mocks/fixtures/sbom-comparison.json`
- Returns 400 if either param is missing

**Mock Fixture** in `tests/mocks/fixtures/sbom-comparison.json`:
Create a fixture matching the `SbomComparison` interface with:
- 2-3 added packages (including one with advisories)
- 1-2 removed packages
- 1-2 version changes (one upgrade, one downgrade)
- 1-2 new vulnerabilities (one with "critical" severity)
- 1 resolved vulnerability
- 1 license change

**E2E Tests** in `tests/e2e/sbom-compare.spec.ts`:
Follow the pattern in `tests/e2e/sbom-list.spec.ts`. Test scenarios:
1. Navigate to `/sbom/compare` — verify empty state is shown
2. Navigate to `/sbom/compare?left={id1}&right={id2}` — verify all diff sections render with correct counts
3. Verify critical vulnerability row has highlighted styling
4. Verify URL-shareable: load page with query params and confirm comparison auto-triggers

**Unit Tests** in `src/pages/SbomComparePage/SbomComparePage.test.tsx`:
Follow the pattern in `src/pages/SbomListPage/SbomListPage.test.tsx`. Use React Testing Library with MSW for API mocking.

## Reuse Candidates
- `tests/mocks/handlers.ts` — existing MSW handler patterns
- `tests/mocks/fixtures/sboms.json` — fixture format reference
- `tests/e2e/sbom-list.spec.ts` — Playwright test patterns and navigation helpers
- `tests/setup.ts` — test setup with MSW and render helpers
- `src/pages/SbomListPage/SbomListPage.test.tsx` — unit test pattern for page components

## Acceptance Criteria
- [ ] MSW handler for comparison endpoint returns mock data
- [ ] MSW handler returns 400 for missing query parameters
- [ ] Mock fixture includes data for all six diff categories
- [ ] E2E test verifies empty state on initial page load
- [ ] E2E test verifies diff sections render with data from URL params
- [ ] E2E test verifies critical vulnerability row highlighting
- [ ] Unit tests cover comparison page rendering with mock data

## Test Requirements
- [ ] E2E: empty state displays without query params
- [ ] E2E: comparison renders correctly with URL params
- [ ] E2E: critical vulnerability highlighting visible
- [ ] Unit: page renders empty state without data
- [ ] Unit: page renders diff sections with mock comparison data

## Verification Commands
- `npx vitest run SbomComparePage` — unit tests pass
- `npx playwright test sbom-compare` — E2E tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch
- Depends on: Task 8 — Frontend comparison page
- Depends on: Task 9 — Frontend SBOM list selection

[sdlc-workflow] Description digest: sha256-md:90a14059d764a8058b724de4bb96f376f1cb590074e7a3093201a9bc0538f000

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add MSW mock handlers, fixture data, and Playwright E2E tests for the SBOM comparison workflow. This provides end-to-end test coverage for the full comparison user flow: selecting SBOMs on the list page, navigating to the comparison page, viewing diff results, and verifying URL shareability.

## Files to Create
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison response data with representative diff entries
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E tests for comparison workflow

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW handler for GET /api/v2/sbom/compare
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for comparison page (created in task 9, test file added here)

## Implementation Notes
**MSW handler** in `tests/mocks/handlers.ts`:
Add a handler for `GET /api/v2/sbom/compare` that returns the fixture data from `sbom-comparison.json`. Follow the existing handler patterns for other endpoints in the same file.

**Fixture data** in `tests/mocks/fixtures/sbom-comparison.json`:
Create a representative comparison response with at least one entry in each diff section (added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, license changes). Include a "critical" severity vulnerability to test the highlighted row styling.

**E2E tests** in `tests/e2e/sbom-compare.spec.ts`:
Follow the existing E2E pattern in `tests/e2e/sbom-list.spec.ts`. Test the full workflow:
1. Navigate to SBOM list, select two SBOMs, click Compare
2. Verify comparison page loads with correct diff sections
3. Navigate directly to `/sbom/compare?left=id1&right=id2` (URL shareability)

Per CONVENTIONS.md §Testing: Vitest + React Testing Library for unit tests; Playwright for E2E; MSW for API mocking. Applies: task creates `tests/e2e/sbom-compare.spec.ts` matching the convention's `.ts` test scope, and modifies `tests/mocks/handlers.ts` matching the convention's `.ts` scope.

## Reuse Candidates
- `tests/mocks/handlers.ts` — existing MSW handlers for pattern reference
- `tests/mocks/fixtures/sboms.json` — existing mock data for SBOM structure reference
- `tests/mocks/fixtures/advisories.json` — existing mock data for advisory structure reference
- `tests/e2e/sbom-list.spec.ts` — existing E2E test for navigation and interaction patterns
- `tests/setup.ts` — test setup with MSW and render helpers

## Dependencies
- Depends on: Task 10 — Frontend routing and list integration (full workflow requires route and list page changes)

## Acceptance Criteria
- [ ] MSW handler for comparison endpoint returns fixture data
- [ ] Fixture data covers all six diff sections with realistic entries
- [ ] E2E test: select two SBOMs on list page, click Compare, verify comparison page loads
- [ ] E2E test: navigate directly to comparison URL, verify page renders with diff data
- [ ] Unit tests for SbomComparePage cover empty state, loading state, and populated state

## Test Requirements
- [ ] E2E test: full comparison workflow from SBOM list to comparison view
- [ ] E2E test: URL shareability — direct navigation to comparison URL renders correctly
- [ ] E2E test: empty state renders when navigating to /sbom/compare without query params
- [ ] Unit test: SbomComparePage renders loading skeletons while API call is in progress
- [ ] Unit test: SbomComparePage renders all six diff sections with mock data
- [ ] Unit test: critical severity rows in New Vulnerabilities section have highlighted styling

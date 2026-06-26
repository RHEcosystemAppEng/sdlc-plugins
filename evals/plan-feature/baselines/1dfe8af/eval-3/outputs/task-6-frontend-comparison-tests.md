## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add MSW mock handlers, test fixtures, and end-to-end tests for the SBOM comparison feature. This ensures the comparison page works correctly across the full user workflow: selecting SBOMs, viewing the comparison, and verifying URL shareability.

## Files to Create
- `tests/mocks/fixtures/sbom-comparison.json` -- Mock comparison API response fixture with representative data across all six diff categories
- `tests/e2e/sbom-compare.spec.ts` -- Playwright E2E tests for the comparison workflow

## Files to Modify
- `tests/mocks/handlers.ts` -- Add MSW handler for `GET /api/v2/sbom/compare` that returns the mock fixture

## Implementation Notes
The MSW handler in `tests/mocks/handlers.ts` should follow the pattern established by existing handlers in that file. Register a `rest.get('/api/v2/sbom/compare', ...)` handler that reads `left` and `right` query parameters and returns the `sbom-comparison.json` fixture. Return 400 if either parameter is missing.

The mock fixture `tests/mocks/fixtures/sbom-comparison.json` should include realistic test data:
- At least 2 added packages, 1 removed package, 1 version change (upgrade), 1 version change (downgrade)
- At least 1 new vulnerability with "critical" severity and 1 with "medium" severity
- At least 1 resolved vulnerability
- At least 1 license change

The E2E tests in `tests/e2e/sbom-compare.spec.ts` should follow the pattern in `tests/e2e/sbom-list.spec.ts` and cover:
1. Navigate to `/sbom/compare` -- verify empty state is shown
2. Select two SBOMs and click Compare -- verify diff sections appear with correct counts
3. Verify URL updates with SBOM IDs after comparison
4. Navigate directly to `/sbom/compare?left=id1&right=id2` -- verify comparison loads automatically
5. Verify Critical severity rows have visual highlighting in New Vulnerabilities section

## Reuse Candidates
- `tests/mocks/handlers.ts` -- Existing MSW handler patterns for API mocking
- `tests/mocks/fixtures/sboms.json` -- Existing fixture format reference
- `tests/e2e/sbom-list.spec.ts` -- Existing E2E test patterns with Playwright
- `tests/setup.ts` -- Test setup configuration with MSW and render helpers

## Acceptance Criteria
- [ ] MSW handler correctly intercepts comparison API calls and returns mock data
- [ ] Mock fixture contains representative data for all six diff categories
- [ ] E2E tests cover the complete comparison workflow from SBOM selection to diff viewing
- [ ] E2E test verifies URL-based comparison loading for shareability
- [ ] All tests pass in CI

## Test Requirements
- [ ] E2E: empty state renders on `/sbom/compare` without query params
- [ ] E2E: comparison renders correctly after selecting SBOMs and clicking Compare
- [ ] E2E: URL includes SBOM IDs after comparison is triggered
- [ ] E2E: direct navigation to comparison URL with query params loads comparison automatically
- [ ] E2E: Critical severity vulnerabilities are visually highlighted

## Dependencies
- Depends on: Task 5 -- Implement SBOM comparison page UI

[sdlc-workflow] Description digest: sha256-md:f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8

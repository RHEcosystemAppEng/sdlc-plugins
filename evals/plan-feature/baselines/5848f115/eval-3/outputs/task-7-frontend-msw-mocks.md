## Repository
trustify-ui

## Target Branch
main

## Description
Add MSW (Mock Service Worker) request handlers and fixture data for the SBOM comparison endpoint. This supports the unit tests for the comparison page and API hook, ensuring tests can run without a live backend.

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW handler for `GET /api/v2/sbom/compare`

## Files to Create
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison result fixture with representative data across all six diff categories
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E test for the SBOM comparison workflow

## Implementation Notes
- Follow the existing MSW handler pattern in `tests/mocks/handlers.ts` which already handles SBOM and advisory endpoints.
- The mock handler should:
  - Match `GET /api/v2/sbom/compare` requests
  - Extract `left` and `right` query parameters
  - Return the `sbom-comparison.json` fixture data
  - Return 400 if either parameter is missing
- The fixture data (`sbom-comparison.json`) should include representative entries in all six sections to enable comprehensive testing:
  - At least 2 added packages (one with advisories)
  - At least 2 removed packages
  - At least 1 version upgrade and 1 version downgrade
  - At least 1 critical and 1 medium new vulnerability
  - At least 1 resolved vulnerability
  - At least 1 license change
- Follow the existing fixture pattern in `tests/mocks/fixtures/sboms.json` and `tests/mocks/fixtures/advisories.json` for data structure.
- The E2E test should cover the full comparison workflow per Use Case UC-1:
  1. Navigate to SBOM list page
  2. Select two SBOMs
  3. Click "Compare selected"
  4. Verify comparison page loads with diff sections
  5. Verify URL contains both SBOM IDs for shareability

## Reuse Candidates
- `tests/mocks/handlers.ts` — existing MSW handlers showing the handler registration pattern
- `tests/mocks/fixtures/sboms.json` — existing SBOM mock data showing fixture format
- `tests/mocks/fixtures/advisories.json` — existing advisory mock data
- `tests/setup.ts` — test setup with MSW configuration and render helpers
- `tests/e2e/sbom-list.spec.ts` — existing Playwright E2E test showing the E2E test pattern

## Acceptance Criteria
- [ ] MSW handler for comparison endpoint is registered in `tests/mocks/handlers.ts`
- [ ] Mock fixture includes representative data in all six diff categories
- [ ] Fixture data matches the SbomComparisonResult TypeScript interface shape
- [ ] E2E test covers the full comparison workflow from SBOM list to comparison view
- [ ] All existing tests continue to pass with the new handler registered

## Test Requirements
- [ ] E2E test: navigate to SBOM list, select two SBOMs, click Compare, verify diff sections render
- [ ] E2E test: verify URL shareability — navigate directly to `/sbom/compare?left=id1&right=id2` and verify comparison loads
- [ ] Unit test: MSW handler returns correct fixture data for valid requests
- [ ] Unit test: MSW handler returns 400 for missing parameters

## Verification Commands
- `npm run test` — all unit tests pass
- `npx playwright test sbom-compare` — E2E tests pass

## Dependencies
- Depends on: Task 5 — Frontend comparison page (page component must exist for E2E testing)
- Depends on: Task 6 — Frontend SBOM list compare action (list page selection must exist for E2E workflow)

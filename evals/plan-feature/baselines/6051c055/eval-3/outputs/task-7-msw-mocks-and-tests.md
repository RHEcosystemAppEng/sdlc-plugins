# Task 7 -- MSW mocks and tests for SBOM comparison

## Repository
trustify-ui

## Target Branch
main

## Description
Add MSW (Mock Service Worker) mock handlers and test fixtures for the SBOM comparison endpoint, and add comprehensive unit tests for the comparison page and its sub-components. The mocks enable isolated frontend testing without a running backend, and the tests verify all user interactions and rendering behavior.

## Files to Create
- `tests/mocks/sbom-comparison-fixtures.ts` -- Test fixture data for SbomComparison responses: a full diff fixture with all six categories populated, an empty diff fixture, and a large diff fixture for performance testing
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` -- Comprehensive unit tests for the comparison page component

## Files to Modify
- `tests/mocks/handlers.ts` -- Add MSW request handler for GET /api/v2/sbom/compare that returns fixture data based on query parameters

## Implementation Notes
- Follow the existing MSW handler pattern in `tests/mocks/handlers.ts` for request matching, parameter extraction, and response format.
- Fixture data should include realistic package names, versions, advisory IDs, severity levels (including at least one "critical" for testing highlighting), and license identifiers.
- The empty diff fixture should have all six arrays empty, simulating comparison of identical SBOMs.
- Per CONVENTIONS.md MSW mocking: test files use MSW handlers for API mocking. Applies: task modifies `tests/mocks/handlers.ts` matching the convention's test mock scope.

## Acceptance Criteria
- [ ] MSW handler intercepts GET /api/v2/sbom/compare requests and returns fixture data
- [ ] Full diff fixture contains representative data for all six diff categories
- [ ] Empty diff fixture returns all-empty arrays
- [ ] All comparison page unit tests pass with MSW mocks

## Test Requirements
- [ ] Test: comparison page renders empty state on initial load (no query params)
- [ ] Test: comparison page renders loading skeletons while API call is in progress
- [ ] Test: comparison page renders all six diff sections with correct data from fixtures
- [ ] Test: DiffSection component expands/collapses correctly
- [ ] Test: Badge counts match the number of items in each diff category
- [ ] Test: critical vulnerability rows in NewVulnerabilitiesTable have highlighted styling
- [ ] Test: Compare button is disabled when fewer than two SBOMs are selected
- [ ] Test: URL parameters are updated when Compare is clicked

## Verification Commands
- `npx vitest run src/pages/SbomComparePage` -- all comparison page tests pass
- `npx tsc --noEmit` -- no TypeScript compilation errors

## Dependencies
- Depends on: Task 5 -- Frontend API types and client for SBOM comparison
- Depends on: Task 6 -- SBOM comparison page component

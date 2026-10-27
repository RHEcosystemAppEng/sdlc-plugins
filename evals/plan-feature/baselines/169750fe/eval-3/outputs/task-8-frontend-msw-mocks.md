## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add MSW request handlers for the comparison endpoint and mock fixture data to support component testing. Create comprehensive test fixtures that cover normal comparison results, empty comparisons, and error responses.

## Files to Modify
- `tests/mocks/handlers.ts` — add MSW handler for GET /api/v2/sbom/compare

## Files to Create
- `tests/mocks/fixtures/sbom-comparison.json` — mock comparison response data with entries in all six diff categories

## Implementation Notes
Follow the existing MSW mock pattern in `tests/mocks/handlers.ts` for request handler definition. The handler should match `GET /api/v2/sbom/compare` and return fixture data from `tests/mocks/fixtures/sbom-comparison.json`.

Reference existing fixtures in `tests/mocks/fixtures/sboms.json` and `tests/mocks/fixtures/advisories.json` for fixture data structure and naming conventions.

The mock fixture should include:
- At least 2 entries in `added_packages`
- At least 2 entries in `removed_packages`
- At least 1 entry in `version_changes`
- At least 1 entry in `new_vulnerabilities` (with severity "critical" for highlight testing)
- At least 1 entry in `resolved_vulnerabilities`
- At least 1 entry in `license_changes`

Per CONVENTIONS.md §Testing: Vitest + React Testing Library for unit tests; MSW for API mocking.
Applies: task modifies `tests/mocks/handlers.ts` matching the convention's TypeScript test file scope.

## Reuse Candidates
- `tests/mocks/handlers.ts` — existing MSW handlers demonstrating the handler definition pattern
- `tests/mocks/fixtures/sboms.json` — existing mock SBOM data for reference fixture structure
- `tests/mocks/fixtures/advisories.json` — existing mock advisory data for reference

## Acceptance Criteria
- [ ] MSW handler intercepts `GET /api/v2/sbom/compare` requests
- [ ] Mock fixture data includes entries in all six diff categories
- [ ] Handler returns appropriate error responses for missing parameters
- [ ] Existing MSW handlers are not broken by the addition

## Test Requirements
- [ ] Component tests for SbomComparePage use the MSW handlers and render correctly with mock data
- [ ] Verify MSW handler returns 400 for missing query parameters

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 7 — Frontend comparison page

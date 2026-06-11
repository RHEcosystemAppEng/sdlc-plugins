# Task 8 — Add MSW mock handlers and test fixtures for SBOM comparison

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add MSW (Mock Service Worker) request handlers and fixture data for the SBOM comparison endpoint to support testing of the comparison page and its components. This ensures all comparison-related unit and integration tests have consistent mock data.

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW handler for `GET /api/v2/sbom/compare` that returns mock comparison data based on query parameters

## Files to Create
- `tests/mocks/fixtures/sbom-comparison.json` — Mock `SbomComparisonResult` fixture with representative data across all six diff categories (added packages, removed packages, version changes, new vulnerabilities with varying severities including critical, resolved vulnerabilities, license changes)

## Implementation Notes
- Follow the existing MSW handler pattern in `tests/mocks/handlers.ts` — use `rest.get` to match the comparison endpoint and return fixture data.
- The handler should parse `left` and `right` query params. Return 400 if either is missing. Return the fixture data for valid requests.
- Fixture data should include:
  - 2-3 added packages with varying advisory counts
  - 1-2 removed packages
  - 2 version changes (one upgrade, one downgrade)
  - 2 new vulnerabilities (one critical severity for highlight testing, one medium)
  - 1 resolved vulnerability
  - 1 license change
- Fixture format must match the `SbomComparisonResult` TypeScript interface exactly.
- Follow the existing fixture patterns in `tests/mocks/fixtures/sboms.json` and `advisories.json` for naming conventions and data realism.

## Reuse Candidates
- `tests/mocks/handlers.ts` — existing MSW handlers for reference pattern
- `tests/mocks/fixtures/sboms.json` — existing SBOM fixture data for consistent naming
- `tests/mocks/fixtures/advisories.json` — existing advisory fixture data for consistent severity values
- `tests/setup.ts` — test setup configuration for MSW integration

## Acceptance Criteria
- [ ] MSW handler intercepts `GET /api/v2/sbom/compare` requests
- [ ] Handler returns 400 when query params are missing
- [ ] Handler returns fixture data for valid requests
- [ ] Fixture data includes all six diff categories with representative entries
- [ ] Fixture includes at least one critical severity vulnerability for highlight testing
- [ ] Fixture format matches `SbomComparisonResult` interface

## Test Requirements
- [ ] Verify MSW handler is registered and responds correctly (this is validated implicitly by the comparison page tests in Task 6)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add frontend API types, client function, and React Query hook for SBOM comparison (interface definitions)

# Task 8 — Add MSW mock handlers and fixtures for the SBOM comparison endpoint

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add Mock Service Worker (MSW) request handlers and fixture data for the `GET /api/v2/sbom/compare` endpoint. These mocks enable unit tests and local development without requiring the backend comparison endpoint to be running.

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW request handler for `GET /api/v2/sbom/compare` that returns fixture data based on `left` and `right` query parameters

## Files to Create
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison result fixture with representative data across all six diff categories

## Implementation Notes
- Follow the existing MSW handler pattern in `tests/mocks/handlers.ts` — use `rest.get()` with the full API path.
- The handler should extract `left` and `right` from the request URL search params and return the fixture data.
- The fixture should include non-empty arrays for all six diff categories to enable comprehensive test coverage:
  - 2-3 added packages, 1-2 removed packages, 2 version changes (one upgrade, one downgrade), 2 new vulnerabilities (one critical, one medium), 1 resolved vulnerability, 1 license change.
- Include a critical-severity vulnerability in the `new_vulnerabilities` array to test the critical highlighting feature.
- Follow the existing fixture pattern in `tests/mocks/fixtures/sboms.json` for data structure and naming conventions.

## Reuse Candidates
- `tests/mocks/handlers.ts` — Existing MSW handlers; follow the same pattern for the new endpoint
- `tests/mocks/fixtures/sboms.json` — Existing mock SBOM data; reference for fixture format
- `tests/mocks/fixtures/advisories.json` — Existing mock advisory data; reference for advisory-related fixture fields
- `tests/setup.ts` — Test setup with MSW; verify the new handler is included in the server setup

## Acceptance Criteria
- [ ] MSW handler intercepts `GET /api/v2/sbom/compare` requests and returns fixture data
- [ ] Fixture contains representative data for all six diff categories
- [ ] Fixture includes at least one critical-severity vulnerability for highlight testing
- [ ] Existing tests continue to pass (no regression from new handler)

## Test Requirements
- [ ] Verify the MSW handler returns correct fixture data when called with valid query params
- [ ] Verify the fixture JSON is valid and matches the `SbomComparisonResult` TypeScript interface

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 6 — Add frontend API types, client function, and React Query hook for SBOM comparison

# Task 7 — Add MSW handlers and mock fixtures for SBOM comparison endpoint

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add Mock Service Worker (MSW) request handlers and mock data fixtures for the SBOM comparison API endpoint. These are needed for unit tests of the comparison page and its components, as well as for local development when the backend comparison endpoint is not yet available.

## Files to Create
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison result data with representative entries for all six diff categories

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW handler for `GET /api/v2/sbom/compare` that returns the mock fixture data

## Implementation Notes
- Follow the existing MSW handler pattern in `tests/mocks/handlers.ts` — handlers use `rest.get()` with path matching and return `res(ctx.json(...))`.
- Follow the existing fixture pattern in `tests/mocks/fixtures/sboms.json` and `tests/mocks/fixtures/advisories.json` — fixtures are JSON files with realistic mock data.
- The mock fixture should include:
  - 2-3 added packages (with varying advisory counts)
  - 2-3 removed packages
  - 2-3 version changes (mix of upgrades and downgrades)
  - 2-3 new vulnerabilities (including at least one Critical severity for testing row highlighting)
  - 1-2 resolved vulnerabilities
  - 1-2 license changes
- The MSW handler should parse `left` and `right` query parameters and return the fixture data regardless of the values (for testing purposes).
- The handler should return 400 if either `left` or `right` is missing, to match the backend behavior.

## Reuse Candidates
- `tests/mocks/handlers.ts` — Existing MSW handlers to follow for pattern consistency
- `tests/mocks/fixtures/sboms.json` — Existing mock SBOM data for realistic package names and versions
- `tests/mocks/fixtures/advisories.json` — Existing mock advisory data for realistic vulnerability entries
- `tests/setup.ts` — Test setup that configures MSW; ensure the new handler is included in the setup

## Acceptance Criteria
- [ ] MSW handler responds to `GET /api/v2/sbom/compare` with mock comparison data
- [ ] Mock fixture includes entries for all six diff categories
- [ ] Handler returns 400 when left or right query param is missing
- [ ] At least one mock vulnerability has "critical" severity for highlight testing
- [ ] Existing tests continue to pass after adding the new handler

## Test Requirements
- [ ] Verify mock handler is registered and returns expected data shape (validated by comparison page tests in Task 5)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add frontend API types, client function, and React Query hook for SBOM comparison

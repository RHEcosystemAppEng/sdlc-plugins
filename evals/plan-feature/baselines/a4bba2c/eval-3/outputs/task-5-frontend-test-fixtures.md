# Task 5 — Add MSW mock handlers and test fixtures for comparison endpoint

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add MSW (Mock Service Worker) request handlers and JSON fixture data for the SBOM comparison endpoint to support unit testing and development of the comparison page. This provides realistic mock data covering all six diff categories (added/removed packages, version changes, new/resolved vulnerabilities, license changes) for use in component tests and local development.

## Files to Modify
- `tests/mocks/handlers.ts` — add MSW handler for `GET /api/v2/sbom/compare` that returns comparison fixture data based on left/right query params

## Files to Create
- `tests/mocks/fixtures/sbom-comparison.json` — fixture data containing a realistic comparison result with entries in all six diff categories, including at least one critical severity vulnerability for highlight testing

## Implementation Notes
- **MSW handler**: add a `rest.get('/api/v2/sbom/compare', ...)` handler in `tests/mocks/handlers.ts` following the same pattern as existing handlers for other endpoints
- **Fixture data shape**: the JSON fixture must match the backend response shape exactly:
  ```json
  {
    "added_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "removed_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "version_changes": [{ "name": "...", "left_version": "...", "right_version": "...", "direction": "upgrade" }],
    "new_vulnerabilities": [{ "advisory_id": "...", "severity": "critical", "title": "...", "affected_package": "..." }],
    "resolved_vulnerabilities": [{ "advisory_id": "...", "severity": "...", "title": "...", "previously_affected_package": "..." }],
    "license_changes": [{ "name": "...", "left_license": "...", "right_license": "..." }]
  }
  ```
- **Test coverage requirements**: include at least one entry in each array, and include at least one critical-severity vulnerability to support testing of the highlight behavior
- **Query param handling**: the MSW handler should read `left` and `right` query params from the request and return 400 if either is missing
- Per docs/constraints.md §2: every commit must reference TC-9003 in the footer, use Conventional Commits, and include `--trailer="Assisted-by: Claude Code"`

## Reuse Candidates
- `tests/mocks/handlers.ts` — existing MSW handlers to follow the same pattern
- `tests/mocks/fixtures/sboms.json` — existing SBOM fixture data as reference for realistic data shape
- `tests/mocks/fixtures/advisories.json` — existing advisory fixture data for reference
- `tests/setup.ts` — test setup patterns for MSW

## Acceptance Criteria
- [ ] MSW handler for `GET /api/v2/sbom/compare` returns fixture data on valid requests
- [ ] MSW handler returns 400 when left or right query params are missing
- [ ] Fixture data includes entries in all six diff categories
- [ ] Fixture data includes at least one critical-severity vulnerability
- [ ] Existing MSW handlers and tests are not broken

## Test Requirements
- [ ] Verify the MSW handler is correctly registered by running existing test suite — no regressions
- [ ] Verify fixture data can be imported and parsed without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
